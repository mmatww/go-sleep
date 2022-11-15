package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"time"

	pb "github.com/mmatww/go-sleep/sleep"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/reflection"
)

var (
	port = flag.Int("port", 7777, "server port")
)

type server struct {
	pb.UnimplementedGoSleepServer
}

func (s *server) Sleep(ctx context.Context, in *pb.SleepRequest) (*pb.SleepReply, error) {
	log.Printf("go-sleep request id '%v' time %d", in.GetId(), in.GetTime())
	time.Sleep(time.Duration(in.GetTime()) * time.Millisecond)
	return &pb.SleepReply{Id: in.GetId(), Time: in.GetTime()}, nil
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf(":%d", *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
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
