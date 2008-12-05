#ifndef _GRASS_RASTER_H
#define _GRASS_RASTER_H

int R_open_driver(void);
void R_close_driver(void);

void R_set_window(double, double, double, double);
void R_get_window(double *, double *, double *, double *);

void R_standard_color(int);
void R_RGB_color(int, int, int);

void R_line_width(double);
void R_erase(void);

void R_pos_abs(double, double);
void R_line_abs(double, double, double, double);
void R_polydots_abs(const double *, const double *, int);
void R_polyline_abs(const double *, const double *, int);
void R_polygon_abs(const double *, const double *, int);
void R_box_abs(double, double, double, double);

void R_begin(void);
void R_move(double, double);
void R_cont(double, double);
void R_close(void);
void R_stroke(void);
void R_fill(void);
void R_point(double, double);

void R_text_size(double, double);
void R_text_rotation(double);
void R_text(const char *);
void R_get_text_box(const char *, double *, double *, double *, double *);

void R_font(const char *);
void R_encoding(const char *);
void R_font_list(char ***, int *);
void R_font_info(char ***, int *);

void R_begin_scaled_raster(int, int[2][2], double[2][2]);
int R_scaled_raster(int, int,
		    const unsigned char *,
		    const unsigned char *,
		    const unsigned char *, const unsigned char *);
void R_end_scaled_raster(void);
void R_bitmap(int, int, int, const unsigned char *);

#endif
