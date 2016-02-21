'use strict';

var addon = require('nad-bindings')('my_addon');

var vector = new addon.NodeVector();
console.log(vector.push([11,11]));
console.log(vector.get());
console.log(vector.push({}));
console.log(vector.get(1));
console.log(vector.size());
console.log(vector.capacity())
