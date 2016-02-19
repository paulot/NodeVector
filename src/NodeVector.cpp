//
//  NodeVector.cpp
//  node
//
//  Created by Paulo Tanaka on 2/14/16.
//
//

#include "NodeVector.hpp"


Nan::Persistent<v8::Function> NodeVector::constructor;

NodeVector::NodeVector() : values() {}

NodeVector::~NodeVector() {}

void NodeVector::Init(v8::Local<v8::Object> exports) {
  Nan::HandleScope scope;

  // Prepare constructor template
  v8::Local<v8::FunctionTemplate> tpl = Nan::New<v8::FunctionTemplate>(New);

  // Sets the js class name of the object
  tpl->SetClassName(Nan::New("NodeVector").ToLocalChecked());

  // Sets the number of fields that we'll tag along in this instance.
  // These are used to append c++ objects to a v8 object, so that they can
  // be used at a later time
  tpl->InstanceTemplate()->SetInternalFieldCount(1);

  // Set the prototype functions for the object
  Nan::SetPrototypeMethod(tpl, "get", Get);
  Nan::SetPrototypeMethod(tpl, "push", Push);
  Nan::SetPrototypeMethod(tpl, "size", Size);
  Nan::SetPrototypeMethod(tpl, "maxSize", MaxSize);
  Nan::SetPrototypeMethod(tpl, "resize", Resize);
  Nan::SetPrototypeMethod(tpl, "capacity", Capacity);
  Nan::SetPrototypeMethod(tpl, "isEmpty", Empty);
  Nan::SetPrototypeMethod(tpl, "reserve", Reserve);
  Nan::SetPrototypeMethod(tpl, "pop", Pop);
  Nan::SetPrototypeMethod(tpl, "set", Set);

  constructor.Reset(tpl->GetFunction());
  exports->Set(Nan::New("NodeVector").ToLocalChecked(), tpl->GetFunction());
}

void NodeVector::New(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  if (args.IsConstructCall()) {
    // Invoked as a constructor
    NodeVector* obj = new NodeVector();
    obj->Wrap(args.This());
    args.GetReturnValue().Set(args.This());
  } else {
    const int argc = 1;
    v8::Local<v8::Value> argv[argc] = { args[0] };
    v8::Local<v8::Function> cons = Nan::New<v8::Function>(constructor);
    args.GetReturnValue().Set(cons->NewInstance(argc, argv));
  }
}

void NodeVector::Get(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());

  int index = args[0]->IsUndefined() ? 0 : args[0]->NumberValue();

  if (index < (int) obj->values.size() and index >= 0) {
    args.GetReturnValue().Set(Nan::New(obj->values[index]));
  }
}

void NodeVector::Push(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());

  Nan::Persistent<v8::Value, v8::CopyablePersistentTraits<v8::Value> > persistent(args[0]);

  obj->values.push_back(persistent);

  // To convert back to a local we could do something like the following:
  // v8::Local<v8::Value> local = v8::Local<v8::Value>::New(v8::Isolate::GetCurrent(), persistent);

  args.GetReturnValue().Set(Nan::New(persistent));
}

void NodeVector::Size(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  args.GetReturnValue().Set(Nan::New((int32_t) obj->values.size()));
}

void NodeVector::MaxSize(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  args.GetReturnValue().Set(Nan::New((int32_t) obj->values.max_size()));
}

void NodeVector::Resize(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  int new_size = args[0]->NumberValue();

  if (not args[0]->IsUndefined()) {
    obj->values.reserve(new_size);
  }
}

void NodeVector::Capacity(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  args.GetReturnValue().Set(Nan::New((int) obj->values.capacity()));
}

void NodeVector::Empty(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  args.GetReturnValue().Set(Nan::New((bool) obj->values.empty()));
}

void NodeVector::Reserve(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  int new_size = args[0]->NumberValue();

  if (not args[0]->IsUndefined()) {
    obj->values.reserve(new_size);
  }
}

void NodeVector::Pop(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());
  if (obj->values.size() > 0) obj->values.pop_back();
}

// Sets the value of the element at index to the value.
void NodeVector::Set(const Nan::FunctionCallbackInfo<v8::Value>& args) {
  NodeVector* obj = ObjectWrap::Unwrap<NodeVector>(args.Holder());

  if (args.Length() < 2) {
    Nan::ThrowTypeError("Function expects 2 arguments (index, value).");
    return;
  }
  int index = args[0]->NumberValue();
  Nan::Persistent<v8::Value, v8::CopyablePersistentTraits<v8::Value> > newValue(args[1]);

  if ((int) obj->values.size() < index) {
    Nan::ThrowError("Given index is larger than size of vector.");
    return;
  }

  obj->values[index] = newValue;
  args.GetReturnValue().Set(Nan::New(newValue));
}