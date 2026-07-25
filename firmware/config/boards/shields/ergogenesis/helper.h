/*
 * https://github.com/urob/zmk-helpers/blob/main/include/zmk-helpers/helper.h
 */

#pragma once

#define ZMK_HELPER_STRINGIFY(x) #x

// Preprocessor mechanism to overload macros, cf. https://stackoverflow.com/a/27051616/6114651
#define VARGS_(_10, _9, _8, _7, _6, _5, _4, _3, _2, _1, N, ...) N
#define VARGS(...) VARGS_(__VA_ARGS__, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
#define CONCAT_(a, b) a##b
#define CONCAT(a, b) CONCAT_(a, b)

/* ZMK_COMBOS */

// #define ALL 0xff
// #if !defined COMBO_TERM
//     #define COMBO_TERM 30
// #endif
// 
// #define ZMK_COMBO(...) CONCAT(ZMK_COMBO_, VARGS(__VA_ARGS__))(__VA_ARGS__)
// #define ZMK_COMBO_3(name, combo_bindings, keypos) \
//     ZMK_COMBO_4(name, combo_bindings, keypos, ALL)
// #define ZMK_COMBO_4(name, combo_bindings, keypos, combo_layers) \
//     ZMK_COMBO_5(name, combo_bindings, keypos, combo_layers, COMBO_TERM)
// #define ZMK_COMBO_5(name, combo_bindings, keypos, combo_layers, combo_timeout) \
//     ZMK_COMBO_6(name, combo_bindings, keypos, combo_layers, combo_timeout, 0)
// #define ZMK_COMBO_6(name, combo_bindings, keypos, combo_layers, combo_timeout, combo_idle) \
//     ZMK_COMBO_7(name, combo_bindings, keypos, combo_layers, combo_timeout, combo_idle, )
// #define ZMK_COMBO_7(name, combo_bindings, keypos, combo_layers, combo_timeout, combo_idle, combo_vaargs) \
//     / { \
//         combos { \
//             compatible = "zmk,combos"; \
//             combo_ ## name { \
//                 timeout-ms = <combo_timeout>; \
//                 bindings = <combo_bindings>; \
//                 key-positions = <keypos>; \
//                 layers = <combo_layers>; \
//                 require-prior-idle-ms = <combo_idle>; \
//                 combo_vaargs \
//             }; \
//         }; \
//     };

