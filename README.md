
## Install required environment dependencies

```sh
pip install -r requirements-dev.txt
conan profile detect
conan remote add redirectory https://conan.jfreeman.dev
```

## Build

```sh
cupcake build
```

## Test

```sh
cupcake test
```

### Run

```sh
cupcake exe
```
