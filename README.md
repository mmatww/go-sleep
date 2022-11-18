# go-sleep

`go-sleep` is a simple GRPC utility server for benchmarcking traffic.

### Snippets

- Update Protobuf
```
GO: protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative sleep/sleep.proto
PY: python3 -m grpc_tools.protoc -I ./sleep --python_out=./extra/pyclient --pyi_out=./extra/pyclient --grpc_python_out=./extra/pyclient ./sleep/sleep.proto
```

- Build and Deploy
```
SERVER: docker build . -t quay.io/marti_martinez/go-sleep:latest && docker push quay.io/marti_martinez/go-sleep:latest && wectl deploy
GHZ: docker build . -t quay.io/marti_martinez/ghz:latest && docker push quay.io/marti_martinez/ghz:latest
PY_CLIENT: docker build . -t quay.io/marti_martinez/pysleep:latest && docker push quay.io/marti_martinez/pysleep:latest
```

- Test once
```
grpcurl -d '{"sleep": 100, "label":"test"}' sre-mmtest-go-sleep-service-0.grpc.phoenix.dev.wwrk.co:443 sleep.GoSleep/Sleep
```

- Test w/ NLB
```
ghz -c 10 -n 100 --proto sleep/sleep.proto --call sleep.GoSleep/Sleep -d '{"label":"external-100ms", "time":100}' sre-mmtest-go-sleep-service-0.grpc.phoenix.dev.wwrk.co:443
```

- Test Service
```
kk port-forward -n sre-mmtest svc/go-sleep-service-0-service 7777:7777
ghz -c 10 -n 100 --insecure --proto sleep/sleep.proto --call sleep.GoSleep/Sleep -d '{"label":"service-100ms", "time":100}' localhost:7777
``` 
