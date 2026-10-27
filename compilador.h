#ifndef COMPILADOR_H
#define COMPILADOR_H

/* Tipos de error que reporta el compilador */
enum { ERR_LEX = 0, ERR_SIN = 1, ERR_SEM = 2, NUM_TIPOS_ERR = 3 };

/* Registra un error (tipo, linea, mensaje con formato printf).
   Se define en lab.y y lo usan el analizador lexico y el sintactico. */
void registrar_error(int tipo, int linea, const char *fmt, ...);

#endif
