//
//  NodeVector.hpp
//  node
//
//  Created by Paulo Tanaka on 2/14/16.
//
//

#ifndef NodeVector_hpp
#define NodeVector_hpp

#include <nan.h>
#include <vector>


class NodeVector : public Nan::ObjectWrap {
public:
  static void Init(v8::Local<v8::Object> exports);

private:
  NodeVector();
  ~NodeVector();

  static void New(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Push(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Get(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Size(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void MaxSize(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Resize(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Capacity(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Empty(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Reserve(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Pop(const Nan::FunctionCallbackInfo<v8::Value>& args);
  static void Set(const Nan::FunctionCallbackInfo<v8::Value>& args);
  
  static Nan::Persistent<v8::Function> constructor;

  std::vector<Nan::Persistent<v8::Value, v8::CopyablePersistentTraits<v8::Value> > > values;
};

#endif /* NodeVector_hpp */
