package main

import (
	"context"
	"flag"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
    pb "github.com/mmatww/go-sleep/sleep"
)

const (
	defaultTimeout = 5
)

var (
	addr = flag.String("addr", "localhost:7777", "connect address")
	id = flag.String("id", "0000", "id")
    millis = flag.Int("time", 100, "sleep time")
)

func main() {
	flag.Parse()
	conn, err := grpc.Dial(*addr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewGoSleepClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(defaultTimeout) * time.Second)
	defer cancel()
    mm := int64(*millis)
	r, err := c.Sleep(ctx, &pb.SleepRequest{Id: *id, Time: mm})
	if err != nil {
		log.Fatalf("error: %v", err)
	}
    log.Printf("go-sleep reply id '%v' time %d", r.GetId(), r.GetTime())
}
