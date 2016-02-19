{
  "targets": [
    { 
      'target_name': 'my_addon',
      'sources': [ 
          './src/my_addon.cc',
          './my-addon.js',
        ],
        'include_dirs': [
          '<!(node -e "require(\'nan\')")',
      ],
    }
  ]
}
