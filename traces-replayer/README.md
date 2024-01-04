
To download new chromedrivers: https://googlechromelabs.github.io/chrome-for-testing/#stable



Inside the *./generalization* folder you can generalize the framework by creating independently the state chart. More informations on it can be found inside the thesis work.

In order to build and run it in your machine, you must have already installed and configured:
- NodeJS v12.20.2
- Puppeteer node module v13.7.0
- fs node module v1.0.0
- is-same-origin node module v0.0.7

Then you can open a terminal inside that folder and run the *main.js* file with NodeJS. You can specify the link to the visualization inside the *./generalization/material/system_url.txt* configuration file, while the list of excluded events can be customized inside the *./generalization/material/excluded_events.txt* configuration file.

<hr> <hr> <hr>

Inside the *./validation* folder you can validate the framework by testing all the interaction paths executable on a visualizaion. 

Work is still in progress, but in order to build and run it in your machine, you must have already installed and configured:
- Selenium package (pip install selenium)
- A Browser WebDriver (it's not important which browser, [here](https://www.youtube.com/watch?v=dz59GsdvUF8) there's a link to a tutorial for Chrome)

In order to validate a visualization you have to:
1. Change value of url, visualization name and sibling percentage in the *conf.json* file
2. Run the PathsGenerator.py file using a terminal or an IDE like VSCode
3. Run the PathsSimulator.py file in the same way

Now you can verify the latencies in the files inside the *resultExplorations* folder, for each interface there will be a file with only the violations (*summaryProblems*) and one with the latency times for each event (*summary*).

<hr> <hr> <hr>


