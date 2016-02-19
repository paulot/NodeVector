#include <nan.h>
#include "NodeVector.hpp"


void InitAll(v8::Local<v8::Object> exports) {
  NodeVector::Init(exports);
}

NODE_MODULE(my_addon, InitAll)