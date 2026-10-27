%option noyywrap yylineno 8bit nounput noinput

%{
/* ===================================================================
   ANALIZADOR LEXICO - Mini lenguaje de incidencias de laboratorio
   Genera tokens y detecta errores lexicos:
     - simbolos no reconocidos
     - identificadores que inician con digito (ej. 2luz)
     - palabras reservadas mal escritas (ej. apagar, Luz)
   =================================================================== */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "compilador.h"
#include "lab.tab.h"

/* Linea del token actual y del anterior (los usa yyerror en lab.y) */
int cur_tok_line = 0, prev_tok_line = 0;

/* Registra la linea del token, la guarda en yylloc y devuelve el token */
#define TOK(t) (prev_tok_line = cur_tok_line, cur_tok_line = yylineno, \
                yylloc.first_line = yylloc.last_line = yylineno, (t))

static const char *RESERVADAS[] = {
    "LUZ", "TEMPERATURA", "SI", "ENTONCES", "ENCENDER", "APAGAR",
    "MOSTRAR", "FIN", "INCIDENTE", "SENSOR", "NIVEL", "REPORTAR",
    "ON", "OFF", NULL
};

/* Compara sin distinguir mayusculas/minusculas */
static int igual_ci(const char *a, const char *b)
{
    while (*a && *b) {
        char x = (*a >= 'a' && *a <= 'z') ? *a - 32 : *a;
        char y = (*b >= 'a' && *b <= 'z') ? *b - 32 : *b;
        if (x != y) return 0;
        a++; b++;
    }
    return *a == *b;
}

/* Si 's' es una reservada escrita con otras mayusculas/minusculas,
   devuelve la forma correcta; si no, NULL */
static const char *reservada_equivalente(const char *s)
{
    int i;
    for (i = 0; RESERVADAS[i]; i++)
        if (igual_ci(s, RESERVADAS[i])) return RESERVADAS[i];
    return NULL;
}
%}

LETRA    [A-Za-z]
DIGITO   [0-9]

%%

[ \t\r]+                     { /* regla 5: los espacios separan tokens */ }
\n                           { /* yylineno se actualiza solo */ }

"LUZ"                        { return TOK(TK_LUZ); }
"TEMPERATURA"                { return TOK(TK_TEMPERATURA); }
"SI"                         { return TOK(TK_SI); }
"ENTONCES"                   { return TOK(TK_ENTONCES); }
"ENCENDER"                   { return TOK(TK_ENCENDER); }
"APAGAR"                     { return TOK(TK_APAGAR); }
"MOSTRAR"                    { return TOK(TK_MOSTRAR); }
"FIN"                        { return TOK(TK_FIN); }
"INCIDENTE"                  { return TOK(TK_INCIDENTE); }
"SENSOR"                     { return TOK(TK_SENSOR); }
"NIVEL"                      { return TOK(TK_NIVEL); }
"REPORTAR"                   { return TOK(TK_REPORTAR); }
"ON"                         { return TOK(TK_ON); }
"OFF"                        { return TOK(TK_OFF); }

"=="|"!="|">="|"<="|">"|"<"  { return TOK(TK_RELOP); }
";"                          { return TOK(TK_SEMI); }

{DIGITO}+                    { yylval.num = (int) strtol(yytext, NULL, 10);
                               return TOK(TK_NUM); }

{DIGITO}+({LETRA}|_)({LETRA}|{DIGITO}|_)* {
                               registrar_error(ERR_LEX, yylineno,
                                   "identificador invalido '%s': no puede iniciar con un digito",
                                   yytext);
                             }

{LETRA}({LETRA}|{DIGITO}|_)* {
                               const char *correcta = reservada_equivalente(yytext);
                               if (correcta) {
                                   registrar_error(ERR_LEX, yylineno,
                                       "palabra reservada mal escrita '%s' (debe ser %s)",
                                       yytext, correcta);
                               } else {
                                   yylval.str = strdup(yytext);
                                   return TOK(TK_ID);
                               }
                             }

[\x80-\xFF]+                 { registrar_error(ERR_LEX, yylineno,
                                   "caracter no valido (fuera de ASCII)"); }

.                            { registrar_error(ERR_LEX, yylineno,
                                   "simbolo no reconocido '%s'", yytext); }

<<EOF>>                      { prev_tok_line = cur_tok_line; return 0; }

%%
