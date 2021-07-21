
pkg = c('shiny', 'shinyWidgets', 'shinythemes', 'shinydashboard', 'DT', 'highcharter', 'dplyr', 'reticulate')
sapply(pkg, require, character.only = TRUE)


py_run_file("buyandhold.py")


# ##############################################################################
# ui
# ##############################################################################
ui <- navbarPage(

    "eunjiJeong729",
    # shinythemes::themeSelector(),
    theme = shinythemes::shinytheme("united"),

    position = "fixed-top",
    header = tagList(
      useShinydashboard()
    ),
    
    # --------------------------------------------------------------------------
    # buyandhold
    # --------------------------------------------------------------------------
    tabPanel("buyandhold",
             tags$head(
               tags$style(HTML("table {
                              font-size:13px;
                            }"))
             ),
             sidebarPanel(
               style = "position:fixed; margin-top:80px; width:300px",
               dateRangeInput('dateRange',
                              label = 'Date range input: yyyy-mm-dd',
                              start = Sys.Date() - 7, end = Sys.Date()
               ),
               br(),
               dateInput('std_dt',
                         label = 'Standard Date',
                         value = Sys.Date()-1),
               br(),br(),br(),br(),br(),
               br(),br(),br(),br(),br()
             ),
             
             # Show a plot of the generated distribution
             mainPanel(
               style = "margin-left:350px; margin-top:80px",
               fluidRow(box(width = 12,
                            infoBoxOutput("ib_CAGR", width = 3),
                            infoBoxOutput("ib_Sharpe", width = 3),
                            infoBoxOutput("ib_VOL", width = 3),
                            infoBoxOutput("ib_MDD", width = 3)
               )),
               highchartOutput("lc_st_rtn", height = "500px"),
               hr(),
               HTML("<font color='red'> ▶ Return Computation </font>"),
               br(),
               DT::dataTableOutput("price_dt_df"),
               HTML("<font color='red'> ▶ Raw Data </font>"),
               br(),
               DT::dataTableOutput("dt_df"),
               br(),br()
             )
    ),
    # --------------------------------------------------------------------------
    # about EJJeong
    # --------------------------------------------------------------------------
    tabPanel("about EJJeong",
             style = "margin-top:80px;",
             includeMarkdown('https://raw.githubusercontent.com/eunjiJeong729/eunjiJeong729/main/README.md')
    )
)


# ##############################################################################
# server
# ##############################################################################
server <- function(input, output) {
  # ----------------------------------------------------------------------------
  # InfoBox
  # ----------------------------------------------------------------------------
  output$ib_CAGR <- renderInfoBox({
    infoBox(
      h5("연평균복리수익률(CAGR)"),
      py$CAGR *100, 
      icon = icon("thumbs-up", lib = "glyphicon"),
      color = "yellow",
      fill = TRUE
    )
  })
  
  output$ib_Sharpe <- renderInfoBox({
    infoBox(
      h5("샤프지수(Sharpe)"),
      py$sharpe *100, 
      icon = icon("refresh"),
      color = "light-blue",
      fill = TRUE
    )
  })
  
  output$ib_VOL <- renderInfoBox({
    infoBox(
      h5("변동성(VOL)"),
      py$VOL *100, 
      icon = icon("list"),
      color = "olive",
      fill = TRUE
    )
  })
  
  output$ib_MDD <- renderInfoBox({
    infoBox(
      h5("MaxDrawDown(MDD)"),
      -1 *py$MDD *100, 
      icon = icon("ok", lib = "glyphicon"),
      color = "red",
      fill = TRUE
    )
  })
  
  # ----------------------------------------------------------------------------
  # Highchart
  # ----------------------------------------------------------------------------
  output$lc_st_rtn <- renderHighchart({
    highchart() %>%
      hc_title(text= "수익률") %>%
      hc_subtitle(text= "st_rtn / daily_rtn") %>%
      hc_xAxis(categories = rownames(py$price_df)) %>%
      hc_yAxis(title = list(text = "Returns")) %>%
      hc_add_series(
        data = (py$price_df[,"st_rtn"] -1) *100,
        type = "line",
        name = "누적수익률"
      ) %>%
      hc_add_series(
        data = py$price_df[,"daily_rtn"] *100,
        type = "line",
        name = "일별수익률"
      ) %>%
      hc_add_series(
        data = -1* py$daily_drawdown *100,
        type = "line",
        name = "daily_drawdown"
      ) %>%
      hc_add_series(
        data = -1* py$historical_dd *100,
        type = "line",
        name = "historical_dd"
      )
  })
  
  # ----------------------------------------------------------------------------
  # DataTable
  # ----------------------------------------------------------------------------
  output$price_dt_df <- DT::renderDataTable(
    DT::datatable({
      py$price_df
    }
    , options = list(scrollX = TRUE, scrollY = TRUE)
    )
  )
  
  output$dt_df <- DT::renderDataTable(
    DT::datatable({
      py$df
    }
    , options = list(scrollX = TRUE, scrollY = TRUE)
    )
  )
}


# ##############################################################################
# shinyApp
# ##############################################################################
shinyApp(ui = ui, server = server)
