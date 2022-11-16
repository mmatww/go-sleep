package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

	pb "github.com/mmatww/go-sleep/sleep"
	netctx "golang.org/x/net/context"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
)

var (
	port = flag.Int("port", 7777, "server port")
)

type server struct {
	pb.UnimplementedGoSleepServer
}

var DefaultXRequestIDKey = "x-request-id"

type requestIDKey struct{}

func FromContext(ctx netctx.Context) string {
	id, ok := ctx.Value(requestIDKey{}).(string)
	if !ok {
		return ""
	}
	return id
}

func HandleRequestID(ctx netctx.Context) string {
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return ""
	}

	header, ok := md[DefaultXRequestIDKey]
	if !ok || len(header) == 0 {
		return ""
	}

	return header[0]
}

func UnaryServerInterceptor() grpc.UnaryServerInterceptor {
	return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
		requestID := HandleRequestID(ctx)
		ctx = context.WithValue(ctx, requestIDKey{}, requestID)
		return handler(ctx, req)
	}
}

func (s *server) Sleep(ctx context.Context, in *pb.SleepRequest) (*pb.SleepReply, error) {
	time.Sleep(time.Duration(in.GetSleep()) * time.Millisecond)
	tt := time.Now().Format(time.UnixDate)
	id := FromContext(ctx)
	ll, _ := json.Marshal(map[string]interface{}{
		"id":        id,
		"label":     in.GetLabel(),
		"sleep":     in.GetSleep(),
		"timestamp": tt,
	})
	log.Printf("%s", ll)

	return &pb.SleepReply{Id: id, Label: in.GetLabel(), Sleep: in.GetSleep(), Timestamp: tt}, nil
}

func main() {
	flag.Parse()
	log.SetFlags(log.Flags() &^ (log.Ldate | log.Ltime))
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	uIntOpt := grpc.UnaryInterceptor(UnaryServerInterceptor())

	s := grpc.NewServer(uIntOpt)
	pb.RegisterGoSleepServer(s, &server{})
	reflection.Register(s)

	healthSrv := health.NewServer()
	healthSrv.SetServingStatus("grpc.health.v1.Health", healthpb.HealthCheckResponse_SERVING)
	healthpb.RegisterHealthServer(s, healthSrv)

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
	log.Printf("server listening at %v", lis.Addr())
}
