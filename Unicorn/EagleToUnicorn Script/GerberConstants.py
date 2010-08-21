
class GerberConstants:

    x_code = "X"
    y_code = "Y"
    c_code = "C"
    
    command_end      = "*" 
    
    # machine codes
    m_code           = "M"
    m_stop           = "00"
    m_optional_stop  = "01"
    m_end            = "02"
    
    #General Functions
    
    g_code                   = "G"
    g_move                   = "00"
    g_linear_1X              = "01"
    g_clockwise_ci           = "02"
    g_counterclockwise_ci    = "03"
    g_ignore_data            = "04"
    g_linear_10X             = "10"
    g_linear_01X             = "11"
    g_linear_001X            = "12"
    g_polygon_fill_on        = "36"
    g_polygon_fill_off       = "37" 
    g_tool_prepare           = "54"
    g_inches                 = "70"
    g_millimeters            = "71"
    g_disable_360_ci         = "74"
    g_enable_360_ci          = "75" 
    g_absolute_format        = "90"
    g_incremental_format     = "91"
    
    #draft codes 
    d_code             = "D"
    d_draw_line        = "01"
    d_exposure_on      = "01"
    d_exposure_off     = "02"
    d_flash_aperature  = "03"
    
    #parameter codes
    p_code             = "%"
    p_apature_definition = "AD" 
    p_apature_macro      = "AM"
    p_axis_select      = "AS"
    p_format_statement = "FS"
    p_mirror_image     = "MI"
    p_mode             = "MO"
    p_offset           = "OF"
    p_scale_factor     = "SF"
    p_image_justify    = "IJ"
    p_image_name       = "IN"
    p_image_offset     = "IO"
    p_image_polarity   = "IP"
    p_image_rotation   = "IR"
    p_plotter_film     = "PF"
    p_layer_polarity   = "LP"

    fs_omit_leading_zeros  = "L"
    fs_omit_trailing_zeros = "T"
    fs_absolute_coords     = "A"
    fs_incremental_coords  = "I"
    fs_N_length            = "N"
    fs_G_length            = "G"
    fs_D_length            = "D"
    fs_M_length            = "M"
    
    ad_circle     = "C"
    ad_rectangle  = "R"
    ad_oval       = "O"
    ad_polygon    = "P"
    

    def __init__():
        return 
   

