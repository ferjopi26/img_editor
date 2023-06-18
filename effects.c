
void convert_to_sepia(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            
            int red = p[0] * 0.393 + p[1] * 0.769 + p[2] * 0.189;
            int green = p[0] * 0.349 + p[1] * 0.686 + p[2] * 0.168;
            int blue = p[0] * 0.272 + p[1] * 0.534 + p[2] * 0.131;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void filter_red(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;

            int red = p[0]*1.10 + p[1]*0.01 + p[2]*0.01;
            int green = p[0]*1.1 + p[1]*0.01 + p[2]*0.01;
            int blue = p[0]*1.1 + p[1]*0.01 + p[2]*0.01;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void filter_green(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;

            int red = p[0]*0.01 + p[1]*1.10 + p[2]*0.01;
            int green = p[0]*0.01 + p[1]*1.10 + p[2]*0.01;
            int blue = p[0]*0.01 + p[1]*1.10 + p[2]*0.01;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void filter_blue(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;

            int red = p[0]*0.01 + p[1]*0.01 + p[2]*1.10;
            int green = p[0]*0.01 + p[1]*0.01 + p[2]*1.10;
            int blue = p[0]*0.01 + p[1]*0.01 + p[2]*1.10;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void filter_yellow(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;

            int red = p[0]*1.10 + p[1]*0.10 + p[2]*0.01;
            int green = p[0]*1.10 + p[1]*0.10 + p[2]*0.01;
            int blue = p[0]*1.10 + p[1]*0.10 + p[2]*0.01;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void filter_orange(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;

            int red = p[0]*1.10 + p[1]*0.01 + p[2]*0.1;
            int green = p[0]*1.10 + p[1]*0.01 + p[2]*0.1;
            int blue = p[0]*1.10 + p[1]*0.01 + p[2]*0.1;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void invert(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    int new_r, new_b, new_g;

    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            
            new_r = 255 - p[0];
            new_g = 255 - p[1];
            new_b = 255 - p[2];

            p[0] = new_r < 0 ? 0 : new_r > 255 ? 255 : new_r;
            p[1] = new_g < 0 ? 0 : new_g > 255 ? 255 : new_g;
            p[2] = new_b < 0 ? 0 : new_b > 255 ? 255 : new_b;
        }
    }
}

void convert_to_gray(unsigned char *pixels, int n_channels, int width, int height, int rowstride)
{
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            
            int red = p[0] * 0.3 + p[1] * 0.59 + p[2] * 0.11;
            int green = p[0] * 0.3 + p[1] * 0.59 + p[2] * 0.11;
            int blue = p[0] * 0.3 + p[1] * 0.59 + p[2] * 0.11;

            p[0] = red > 255 ? 255 : red;
            p[1] = green > 255 ? 255 :green;
            p[2] = blue > 255 ? 255 : blue;
        }
    }
}

void adjust_brightness(unsigned char *pixels, unsigned char *new_pixels, int n_channels, int width, int height, int rowstride, double value)
{
    int new_r, new_b, new_g;
    
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            unsigned char *np = new_pixels + y * rowstride + x * n_channels;

            new_r = p[0]*value;
            new_g = p[1]*value;
            new_b = p[2]*value;

            np[0] = new_r > 255 ? 255 : new_r;
            np[1] = new_g > 255 ? 255 : new_g;
            np[2] = new_b > 255 ? 255 : new_b;
        }
    }
}

void adjust_contrast(unsigned char *pixels, unsigned char *new_pixels, int n_channels, int width, int height, int rowstride, double value)
{
    int new_r, new_b, new_g;
    
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            unsigned char *np = new_pixels + y * rowstride + x * n_channels;

            new_r = p[0] + (255 * value);
            new_g = p[1] + (255 * value);
            new_b = p[2] + (255 * value);

            np[0] = new_r < 0 ? 0 : new_r > 255 ? 255 : new_r;
            np[1] = new_g < 0 ? 0 : new_g > 255 ? 255 : new_g;
            np[2] = new_b < 0 ? 0 : new_b > 255 ? 255 : new_b;
        }
    }
}

void adjust_saturation(unsigned char *pixels, unsigned char *new_pixels, int n_channels, int width, int height, int rowstride, double value)
{
    int new_r, new_b, new_g;
    
    for(int x = 0; x < width; x++)
    {
        for(int y = 0; y < height; y++)
        {
            unsigned char *p = pixels + y * rowstride + x * n_channels;
            unsigned char *np = new_pixels + y * rowstride + x * n_channels;

            float gray = 0.3*p[0] + 0.59*p[1] + 0.11*p[2];

            new_r = -gray * value + p[0] * (1+value);
            new_g = -gray * value + p[1] * (1+value);
            new_b = -gray * value + p[2] * (1+value);

            np[0] = new_r < 0 ? 0 : new_r > 255 ? 255 : new_r;
            np[1] = new_g < 0 ? 0 : new_g > 255 ? 255 : new_g;
            np[2] = new_b < 0 ? 0 : new_b > 255 ? 255 : new_b;
        }
    }
}

/* gcc -fPIC -shared -o effects.so effects.c */

/* 

*/