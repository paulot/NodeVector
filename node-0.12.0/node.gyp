{
  "variables": {
    "node_shared_openssl%": "false",
    "node_use_etw%": "false",
    "node_has_winsdk%": "false",
    "node_shared_http_parser%": "false",
    "node_use_dtrace%": "false",
    "node_shared_v8%": "false",
    "v8_use_snapshot%": "true",
    "node_v8_options%": "",
    "node_use_openssl%": "true",
    "node_shared_zlib%": "false",
    "node_use_mdb%": "false",
    "node_use_perfctr%": "false",
    "library_files": [
      "src/node.js",
      "lib/_debugger.js",
      "lib/_linklist.js",
      "lib/assert.js",
      "lib/buffer.js",
      "lib/child_process.js",
      "lib/console.js",
      "lib/constants.js",
      "lib/crypto.js",
      "lib/cluster.js",
      "lib/dgram.js",
      "lib/dns.js",
      "lib/domain.js",
      "lib/events.js",
      "lib/freelist.js",
      "lib/fs.js",
      "lib/http.js",
      "lib/_http_agent.js",
      "lib/_http_client.js",
      "lib/_http_common.js",
      "lib/_http_incoming.js",
      "lib/_http_outgoing.js",
      "lib/_http_server.js",
      "lib/https.js",
      "lib/module.js",
      "lib/net.js",
      "lib/os.js",
      "lib/path.js",
      "lib/punycode.js",
      "lib/querystring.js",
      "lib/readline.js",
      "lib/repl.js",
      "lib/smalloc.js",
      "lib/stream.js",
      "lib/_stream_readable.js",
      "lib/_stream_writable.js",
      "lib/_stream_duplex.js",
      "lib/_stream_transform.js",
      "lib/_stream_passthrough.js",
      "lib/string_decoder.js",
      "lib/sys.js",
      "lib/timers.js",
      "lib/tls.js",
      "lib/_tls_common.js",
      "lib/_tls_legacy.js",
      "lib/_tls_wrap.js",
      "lib/tty.js",
      "lib/url.js",
      "lib/util.js",
      "lib/vm.js",
      "lib/zlib.js",
      "deps/debugger-agent/lib/_debugger_agent.js"
    ],
    "node_shared_libuv%": "false",
    "node_shared_cares%": "false",
    "my_addon_addon%": "true",
    "module_root_dir%": "/Users/ptanaka/my-addon"
  },
  "targets": [
    {
      "target_name": "node",
      "conditions": [
        [
          "my_addon_addon==\"true\"",
          {
            "sources": [
              "../src/my_addon.cc",
              "../my-addon.js",
              "../binding.gyp"
            ],
            "include_dirs": [
              "<!(node -e \"require('nan')\")"
            ],
            "defines": [
              "MY_ADDON_ADDON"
            ]
          }
        ],
        [
          "gcc_version<=44",
          {
            "cflags": [
              "-fno-strict-aliasing"
            ]
          }
        ],
        [
          "v8_enable_i18n_support==1",
          {
            "dependencies": [
              "<(icu_gyp_path):icui18n",
              "<(icu_gyp_path):icuuc"
            ],
            "conditions": [
              [
                "icu_small==\"true\"",
                {
                  "defines": [
                    "NODE_HAVE_SMALL_ICU=1"
                  ]
                }
              ]
            ],
            "defines": [
              "NODE_HAVE_I18N_SUPPORT=1"
            ]
          }
        ],
        [
          "node_use_openssl==\"true\"",
          {
            "sources": [
              "src/node_crypto.cc",
              "src/node_crypto_bio.cc",
              "src/node_crypto_clienthello.cc",
              "src/node_crypto.h",
              "src/node_crypto_bio.h",
              "src/node_crypto_clienthello.h",
              "src/tls_wrap.cc",
              "src/tls_wrap.h"
            ],
            "conditions": [
              [
                "node_shared_openssl==\"false\"",
                {
                  "dependencies": [
                    "./deps/openssl/openssl.gyp:openssl",
                    "./deps/openssl/openssl.gyp:openssl-cli"
                  ],
                  "conditions": [
                    [
                      "OS in \"linux freebsd\"",
                      {
                        "ldflags": [
                          "-Wl,--whole-archive <(PRODUCT_DIR)/libopenssl.a -Wl,--no-whole-archive"
                        ]
                      }
                    ]
                  ],
                  "xcode_settings": {
                    "OTHER_LDFLAGS": [
                      "-Wl,-force_load,<(PRODUCT_DIR)/libopenssl.a"
                    ]
                  }
                }
              ]
            ],
            "defines": [
              "HAVE_OPENSSL=1"
            ]
          },
          {
            "defines": [
              "HAVE_OPENSSL=0"
            ]
          }
        ],
        [
          "node_use_dtrace==\"true\"",
          {
            "sources": [
              "src/node_dtrace.cc"
            ],
            "include_dirs": [
              "<(SHARED_INTERMEDIATE_DIR)"
            ],
            "dependencies": [
              "node_dtrace_header",
              "specialize_node_d"
            ],
            "conditions": [
              [
                "OS==\"linux\"",
                {
                  "sources": [
                    "<(SHARED_INTERMEDIATE_DIR)/node_dtrace_provider.o"
                  ]
                }
              ],
              [
                "OS!=\"mac\" and OS!=\"linux\"",
                {
                  "sources": [
                    "src/node_dtrace_ustack.cc",
                    "src/node_dtrace_provider.cc"
                  ]
                }
              ]
            ],
            "defines": [
              "HAVE_DTRACE=1"
            ]
          }
        ],
        [
          "node_use_mdb==\"true\"",
          {
            "sources": [
              "src/node_mdb.cc"
            ],
            "dependencies": [
              "node_mdb"
            ],
            "include_dirs": [
              "<(SHARED_INTERMEDIATE_DIR)"
            ]
          }
        ],
        [
          "node_use_etw==\"true\"",
          {
            "sources": [
              "src/node_win32_etw_provider.h",
              "src/node_win32_etw_provider-inl.h",
              "src/node_win32_etw_provider.cc",
              "src/node_dtrace.cc",
              "tools/msvs/genfiles/node_etw_provider.h",
              "tools/msvs/genfiles/node_etw_provider.rc"
            ],
            "dependencies": [
              "node_etw"
            ],
            "defines": [
              "HAVE_ETW=1"
            ]
          }
        ],
        [
          "node_use_perfctr==\"true\"",
          {
            "sources": [
              "src/node_win32_perfctr_provider.h",
              "src/node_win32_perfctr_provider.cc",
              "src/node_counters.cc",
              "src/node_counters.h",
              "tools/msvs/genfiles/node_perfctr_provider.rc"
            ],
            "dependencies": [
              "node_perfctr"
            ],
            "defines": [
              "HAVE_PERFCTR=1"
            ]
          }
        ],
        [
          "v8_postmortem_support==\"true\"",
          {
            "dependencies": [
              "deps/v8/tools/gyp/v8.gyp:postmortem-metadata"
            ],
            "xcode_settings": {
              "OTHER_LDFLAGS": [
                "-Wl,-force_load,<(V8_BASE)"
              ]
            }
          }
        ],
        [
          "node_shared_v8==\"false\"",
          {
            "sources": [
              "deps/v8/include/v8.h",
              "deps/v8/include/v8-debug.h"
            ],
            "dependencies": [
              "deps/v8/tools/gyp/v8.gyp:v8"
            ]
          }
        ],
        [
          "node_shared_zlib==\"false\"",
          {
            "dependencies": [
              "deps/zlib/zlib.gyp:zlib"
            ]
          }
        ],
        [
          "node_shared_http_parser==\"false\"",
          {
            "dependencies": [
              "deps/http_parser/http_parser.gyp:http_parser"
            ]
          }
        ],
        [
          "node_shared_cares==\"false\"",
          {
            "dependencies": [
              "deps/cares/cares.gyp:cares"
            ]
          }
        ],
        [
          "node_shared_libuv==\"false\"",
          {
            "dependencies": [
              "deps/uv/uv.gyp:libuv"
            ]
          }
        ],
        [
          "OS==\"win\"",
          {
            "libraries": [
              "-lpsapi.lib"
            ],
            "sources": [
              "src/res/node.rc"
            ],
            "defines": [
              "FD_SETSIZE=1024",
              "PLATFORM=\"win32\"",
              "_UNICODE=1"
            ]
          },
          {
            "defines": [
              "__POSIX__"
            ]
          }
        ],
        [
          "OS==\"mac\"",
          {
            "libraries": [
              "-framework CoreFoundation"
            ],
            "defines!": [
              "PLATFORM=\"mac\""
            ],
            "defines": [
              "PLATFORM=\"darwin\""
            ]
          }
        ],
        [
          "OS==\"freebsd\"",
          {
            "libraries": [
              "-lutil",
              "-lkvm"
            ]
          }
        ],
        [
          "OS==\"solaris\"",
          {
            "libraries": [
              "-lkstat",
              "-lumem"
            ],
            "defines!": [
              "PLATFORM=\"solaris\""
            ],
            "defines": [
              "PLATFORM=\"sunos\""
            ]
          }
        ],
        [
          "OS in \"linux freebsd\" and node_shared_v8==\"false\"",
          {
            "ldflags": [
              "-Wl,--whole-archive <(V8_BASE) -Wl,--no-whole-archive"
            ]
          }
        ]
      ],
      "msvs_settings": {
        "VCManifestTool": {
          "EmbedManifest": "true",
          "AdditionalManifestFiles": "src/res/node.exe.extra.manifest"
        },
        "VCLinkerTool": {
          "SubSystem": 1
        }
      },
      "sources": [
        "src/async-wrap.cc",
        "src/fs_event_wrap.cc",
        "src/cares_wrap.cc",
        "src/handle_wrap.cc",
        "src/node.cc",
        "src/node_buffer.cc",
        "src/node_constants.cc",
        "src/node_contextify.cc",
        "src/node_file.cc",
        "src/node_http_parser.cc",
        "src/node_javascript.cc",
        "src/node_main.cc",
        "src/node_os.cc",
        "src/node_v8.cc",
        "src/node_stat_watcher.cc",
        "src/node_watchdog.cc",
        "src/node_zlib.cc",
        "src/node_i18n.cc",
        "src/pipe_wrap.cc",
        "src/signal_wrap.cc",
        "src/smalloc.cc",
        "src/spawn_sync.cc",
        "src/string_bytes.cc",
        "src/stream_wrap.cc",
        "src/tcp_wrap.cc",
        "src/timer_wrap.cc",
        "src/tty_wrap.cc",
        "src/process_wrap.cc",
        "src/udp_wrap.cc",
        "src/uv.cc",
        "src/async-wrap.h",
        "src/async-wrap-inl.h",
        "src/base-object.h",
        "src/base-object-inl.h",
        "src/env.h",
        "src/env-inl.h",
        "src/handle_wrap.h",
        "src/node.h",
        "src/node_buffer.h",
        "src/node_constants.h",
        "src/node_file.h",
        "src/node_http_parser.h",
        "src/node_internals.h",
        "src/node_javascript.h",
        "src/node_root_certs.h",
        "src/node_version.h",
        "src/node_watchdog.h",
        "src/node_wrap.h",
        "src/node_i18n.h",
        "src/pipe_wrap.h",
        "src/queue.h",
        "src/smalloc.h",
        "src/tty_wrap.h",
        "src/tcp_wrap.h",
        "src/udp_wrap.h",
        "src/req_wrap.h",
        "src/string_bytes.h",
        "src/stream_wrap.h",
        "src/tree.h",
        "src/util.h",
        "src/util-inl.h",
        "src/util.cc",
        "deps/http_parser/http_parser.h",
        "<(SHARED_INTERMEDIATE_DIR)/node_natives.h",
        "<@(library_files)",
        "common.gypi"
      ],
      "dependencies": [
        "node_js2c#host",
        "deps/debugger-agent/debugger-agent.gyp:debugger-agent"
      ],
      "include_dirs": [
        "src",
        "tools/msvs/genfiles",
        "deps/uv/src/ares",
        "<(SHARED_INTERMEDIATE_DIR)"
      ],
      "type": "executable",
      "defines": [
        "NODE_WANT_INTERNALS=1",
        "ARCH=\"<(target_arch)\"",
        "PLATFORM=\"<(OS)\"",
        "NODE_TAG=\"<(node_tag)\"",
        "NODE_V8_OPTIONS=\"<(node_v8_options)\""
      ]
    },
    {
      "target_name": "node_etw",
      "conditions": [
        [
          "node_use_etw==\"true\" and node_has_winsdk==\"true\"",
          {
            "actions": [
              {
                "action": [
                  "mc <@(_inputs) -h tools/msvs/genfiles -r tools/msvs/genfiles"
                ],
                "inputs": [
                  "src/res/node_etw_provider.man"
                ],
                "outputs": [
                  "tools/msvs/genfiles/node_etw_provider.rc",
                  "tools/msvs/genfiles/node_etw_provider.h",
                  "tools/msvs/genfiles/node_etw_providerTEMP.BIN"
                ],
                "action_name": "node_etw"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "node_perfctr",
      "conditions": [
        [
          "node_use_perfctr==\"true\" and node_has_winsdk==\"true\"",
          {
            "actions": [
              {
                "action": [
                  "ctrpp <@(_inputs) -o tools/msvs/genfiles/node_perfctr_provider.h -rc tools/msvs/genfiles/node_perfctr_provider.rc"
                ],
                "inputs": [
                  "src/res/node_perfctr_provider.man"
                ],
                "outputs": [
                  "tools/msvs/genfiles/node_perfctr_provider.h",
                  "tools/msvs/genfiles/node_perfctr_provider.rc",
                  "tools/msvs/genfiles/MSG00001.BIN"
                ],
                "action_name": "node_perfctr_man"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "node_js2c",
      "toolsets": [
        "host"
      ],
      "type": "none",
      "actions": [
        {
          "action": [
            "<(python)",
            "tools/js2c.py",
            "<@(_outputs)",
            "<@(_inputs)"
          ],
          "inputs": [
            "<@(library_files)",
            "./config.gypi"
          ],
          "conditions": [
            [
              "node_use_dtrace==\"false\" and node_use_etw==\"false\"",
              {
                "inputs": [
                  "src/notrace_macros.py"
                ]
              }
            ],
            [
              "node_use_perfctr==\"false\"",
              {
                "inputs": [
                  "src/perfctr_macros.py"
                ]
              }
            ]
          ],
          "outputs": [
            "<(SHARED_INTERMEDIATE_DIR)/node_natives.h"
          ],
          "action_name": "node_js2c"
        }
      ]
    },
    {
      "target_name": "node_dtrace_header",
      "conditions": [
        [
          "node_use_dtrace==\"true\"",
          {
            "actions": [
              {
                "action": [
                  "dtrace",
                  "-h",
                  "-xnolibs",
                  "-s",
                  "<@(_inputs)",
                  "-o",
                  "<@(_outputs)"
                ],
                "inputs": [
                  "src/node_provider.d"
                ],
                "outputs": [
                  "<(SHARED_INTERMEDIATE_DIR)/node_provider.h"
                ],
                "action_name": "node_dtrace_header"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "node_mdb",
      "conditions": [
        [
          "node_use_mdb==\"true\"",
          {
            "dependencies": [
              "deps/mdb_v8/mdb_v8.gyp:mdb_v8"
            ],
            "actions": [
              {
                "inputs": [
                  "<(PRODUCT_DIR)/obj.target/deps/mdb_v8/mdb_v8.so"
                ],
                "conditions": [
                  [
                    "target_arch==\"ia32\"",
                    {
                      "action": [
                        "elfwrap",
                        "-o",
                        "<@(_outputs)",
                        "<@(_inputs)"
                      ]
                    }
                  ],
                  [
                    "target_arch==\"x64\"",
                    {
                      "action": [
                        "elfwrap",
                        "-64",
                        "-o",
                        "<@(_outputs)",
                        "<@(_inputs)"
                      ]
                    }
                  ]
                ],
                "outputs": [
                  "<(PRODUCT_DIR)/obj.target/node/src/node_mdb.o"
                ],
                "action_name": "node_mdb"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "node_dtrace_provider",
      "conditions": [
        [
          "node_use_dtrace==\"true\" and OS!=\"mac\" and OS!=\"linux\"",
          {
            "actions": [
              {
                "action": [
                  "dtrace",
                  "-G",
                  "-xnolibs",
                  "-s",
                  "src/node_provider.d",
                  "<@(_inputs)",
                  "-o",
                  "<@(_outputs)"
                ],
                "inputs": [
                  "<(OBJ_DIR)/node/src/node_dtrace.o"
                ],
                "outputs": [
                  "<(OBJ_DIR)/node/src/node_dtrace_provider.o"
                ],
                "action_name": "node_dtrace_provider_o"
              }
            ]
          }
        ],
        [
          "node_use_dtrace==\"true\" and OS==\"linux\"",
          {
            "actions": [
              {
                "action": [
                  "dtrace",
                  "-C",
                  "-G",
                  "-s",
                  "<@(_inputs)",
                  "-o",
                  "<@(_outputs)"
                ],
                "inputs": [
                  "src/node_provider.d"
                ],
                "outputs": [
                  "<(SHARED_INTERMEDIATE_DIR)/node_dtrace_provider.o"
                ],
                "action_name": "node_dtrace_provider_o"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "node_dtrace_ustack",
      "conditions": [
        [
          "node_use_dtrace==\"true\" and OS!=\"mac\" and OS!=\"linux\"",
          {
            "actions": [
              {
                "action": [
                  "tools/genv8constants.py",
                  "<@(_outputs)",
                  "<@(_inputs)"
                ],
                "inputs": [
                  "<(V8_BASE)"
                ],
                "outputs": [
                  "<(SHARED_INTERMEDIATE_DIR)/v8constants.h"
                ],
                "action_name": "node_dtrace_ustack_constants"
              },
              {
                "inputs": [
                  "src/v8ustack.d",
                  "<(SHARED_INTERMEDIATE_DIR)/v8constants.h"
                ],
                "conditions": [
                  [
                    "target_arch==\"ia32\"",
                    {
                      "action": [
                        "dtrace",
                        "-32",
                        "-I<(SHARED_INTERMEDIATE_DIR)",
                        "-Isrc",
                        "-C",
                        "-G",
                        "-s",
                        "src/v8ustack.d",
                        "-o",
                        "<@(_outputs)"
                      ]
                    }
                  ],
                  [
                    "target_arch==\"x64\"",
                    {
                      "action": [
                        "dtrace",
                        "-64",
                        "-I<(SHARED_INTERMEDIATE_DIR)",
                        "-Isrc",
                        "-C",
                        "-G",
                        "-s",
                        "src/v8ustack.d",
                        "-o",
                        "<@(_outputs)"
                      ]
                    }
                  ]
                ],
                "outputs": [
                  "<(OBJ_DIR)/node/src/node_dtrace_ustack.o"
                ],
                "action_name": "node_dtrace_ustack"
              }
            ]
          }
        ]
      ],
      "type": "none"
    },
    {
      "target_name": "specialize_node_d",
      "conditions": [
        [
          "node_use_dtrace==\"true\"",
          {
            "actions": [
              {
                "action": [
                  "tools/specialize_node_d.py",
                  "<@(_outputs)",
                  "<@(_inputs)",
                  "<@(OS)",
                  "<@(target_arch)"
                ],
                "inputs": [
                  "src/node.d"
                ],
                "outputs": [
                  "<(PRODUCT_DIR)/node.d"
                ],
                "action_name": "specialize_node_d"
              }
            ]
          }
        ]
      ],
      "type": "none"
    }
  ]
}