syntax keyword apconfKeywords
    \ def
    \ end
    \ req
    \ resp
    \ from
    \ if

syntax keyword apconfInstructions
    \ append
    \ delete
    \ set
    \ replace
    \ intercept
    \ serve

syn keyword apconfBuiltin
    \ METHOD
    \ SCHEME # PROTOCOL?
    \ DOMAIN # HOST?
    \ PORT
    \ PATH
    \ PARAMETERS
    \ VERSION
    \ HEADER
    \ BODY #??
    \ STATUS_CODE
    \ STATUS_MESSAGE
    \ SCOPE

syntax match apconfNumber "#\d\+"

syntax match apconfOperator "&\||\|!\|like\|is\|not\|:\|="
syntax match apconfComment "//.*$"


" https://github.com/egberts/vim-syntax-bind-named/blob/master/syntax/bindzone.vim
syn match       apconfIPAddr              /\v<[0-9]{1,3}(.[0-9]{1,3}){,3}>/

"   Plain IPv6 address          IPv6-embedded-IPv4 address
"   ::[...:]8                   ::[...:]127.0.0.1
syn match       apconfIP6Addr             /\v\s@<=::((\x{1,4}:){,5}([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,6}\x{1,4})>/
"   1111::[...:]8               1111::[...:]127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){1}:((\x{1,4}:){,4}([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,5}\x{1,4})>/
"   1111:2::[...:]8             1111:2::[...:]127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){2}:((\x{1,4}:){,3}([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,4}\x{1,4})>/
"   1111:2:3::[...:]8           1111:2:3::[...:]127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){3}:((\x{1,4}:){,2}([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,3}\x{1,4})>/
"   1111:2:3:4::[...:]8         1111:2:3:4::[...:]127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){4}:((\x{1,4}:){,1}([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,2}\x{1,4})>/
"   1111:2:3:4:5::[...:]8       1111:2:3:4:5::127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){5}:(([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2}|(\x{1,4}:){,1}\x{1,4})>/
"   1111:2:3:4:5:6:7:8          1111:2:3:4:5:6:127.0.0.1
syn match       apconfIP6Addr             /\v<(\x{1,4}:){6}(\x{1,4}:\x{1,4}|([0-2]?\d{1,2}\.){3}[0-2]?\d{1,2})>/
"   1111:2:3:4:5:6::8           -
syn match       apconfIP6Addr             /\v<(\x{1,4}:){6}:\x{1,4}>/
"   1111[:...]::                -
syn match       apconfIP6Addr             /\v<(\x{1,4}:){1,7}:(\s|;|$)@=/
syntax region apconfString start=+[uU]\=\z(["]\)+ end="\z1" skip="\\\\\|\\\z1"

hi def link apconfKeywords Keyword
hi def link apconfBuiltin Type
hi def link apconfNumber Number
hi def link apconfOperator Operator
hi def link apconfComment Comment
hi def link apconfIPAddr Number
hi def link apconfIP6Addr Number
hi def link apconfString String
hi def link apconfInstructions Function
