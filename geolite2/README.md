# GeoLite2 Analysis

### Goal

Looking for answers to how the data is structured.

### Dataset

This analysis used the 6th October 2026 release of the GeoLite2 City CSV dataset, provided by MaxMind.

### Outcome

Any block with a geoname_id is at the very least guaranteed to have coordinates and a continent. On their own, those are meaningless a the accuracy will be 1000 or more.

Location blocks are broken down into continent, country, subdivision 1, subdivision 2, and city

A location block is at least guaranteed the continent.

My findings so far are:

- If a city is present, then a country is also present.
- If subdivision 1 is present, then the country is also present.
- If subdivision 2 is present, then subdivision 1 and country are also present.
- The presence of a city does not imply the presence of subdivisions.

As a table relating the presence of each datapoint to that of the others:

| Datapoint | City | Subdivision 2 | Subdivision 1 | Country | Continent |
| --- | --- | --- | --- | --- | --- |
| City | ✅ | ? | ? | ✅ | ✅ |
| Subdivision 1 | ? | ? | ✅ | ✅ | ✅ |
| Subdivision 2 | ? | ✅ | ✅ | ✅ | ✅ |
| Country | ? | ? | ? | ✅ | ✅ |
| Continent | ? | ? | ? | ? | ✅ |

Given we want to display the most specific possible combination of datapoints to the user, it is proposed that we use:

- City, Country
- Subdivision 2, Subdivision 1, Country
- Subdivision 1, Country
- Country, Continent
- Continent

In order of most to least specific.

`accuracy_radius` is a value from 1 to 1000, denominated in kilometres, that tells us how confident MaxMind are. A value of 200 or more renders a particular location relatively meaningless. In that situation, propose we state "(Estimated)".
