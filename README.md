# UOCIS322 - Project 4 #
Brevet time calculator.

## Maintainer

Ethan Killen
ekillen@uoregon.edu
killen.ethan@gmail.com
541-221-0338

## Overview

Provides a lightweight webserver for a RUSA ACP controle time calculator with flask and ajax.

## Webpage

Contains a table of with columns for distance, location, and opening/closing times for each controle.
Entering data into the distance columns will autofill the opening and closing times for that controle.

## Breakdown

- app.ini: Provides a fallback configuration file.
- credentials-skel.ini: Provides a template credentials config file for the serverhost to fill out.
- flask_brevets.py: Contains the bulk of the code for the webserver.
- src/acp_times.py: Contains the algorythm for calculating ACP Controle times.
- src/config.py: Contains the configuration parsing algorythm.
- templates/...: Contains the website page templates.

## Algorithm

The opening and closing times of each controle are calculated based on the distance into the race the controle is and the maximum/minimum allowed speeds over that distance. The brevet is split into segments from 0-60km, 60-200km, 200-400km, 400-600km, and 600-1000km. Each segment has its own minimum and maximum speeds. The opening time for a controle is the minimum amount of time it would be possible to reach that control in while staying within the alloted speed limits for each brevet segment. Similarly, closing times are calculated as being the maximum possible amount of time it could take to reach the controle within the speed limits of each segment plus an extra hour to make controles sufficiently close to the beginning of the race not close before they open.

In short, the algorithm is:
1. Start with either no time or an hour depending on whether we're calculating opening/closing times.
2. Iterate over each segment of the brevet.
3. Add the amount of time required to travel the length of the segment (current segment distance - previous segment distance) / relevant travel speed
3. - For the first segment 0 is considered the last segment distance.
3. - If the current segment contains the controle distance that is considered as the current segment distance.
4. If we reach the end of the brevet, stop. Distances past the end of the brevet are ignored.

### ACP controle times

That's *"controle"* with an *e*, because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.

The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here [https://rusa.org/pages/rulesForRiders](https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly.  

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data.  

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.
