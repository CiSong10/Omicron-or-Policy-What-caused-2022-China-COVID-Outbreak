# Omicron or Policy: What caused 2022 China COVID outbreak?

This project crawled covid case data from China Nathional Health Commission, including "local new cases" and "imported new cases" from Oct 2020 to Dec 2022.

Data analyses are conducted to find out the reason of China's COVID case increase in 2022.

## Background

China has been stuck to Zero-COVID policy since the COVID-19 pandemic. 
It worked relatively well at first. 
However, people find that the number of covid cases has been rising for months since summer 2022. 
Some people claim that it is due to the decrease in entry quarantine time according to “Guidance for COVID-19 Control (**9th Edition**)”; 
while other people believe it is because the SARS-CoV-2 **Omicron** variant spread more quickly. 

## Data Source

* Crawled covid case data from Oct 2020 to Dec 2022 
from China [National Health Commission](http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml);

* [Coronavirus (COVID-19) Cases - Our World in Data](https://ourworldindata.org/covid-cases).

## Findings

* *Day of the week effect* is not significant: there is not a significant difference between local cases on the weekend and the weekdays.

* There **is** a significant difference in the **total** & **imported** covid case between before and after China’s first **omicron** case;

* There **is** a statistically significant difference in the **imported** covid case between before and after “**9th Edition**” published;

* There **is not** a statistically significant difference in the **total** covid case between before and after “**9th Edition**” published.

## Discussion

Omicron causes the China COVID outbreak in 2022. 
“9th Edition” does increase imported cases but not total cases.
I guess this is because imported cases are test positive during quarantine,
so they are not the reason of the local case outbreak
– That’s just the omicron.

## Contact

Ci 'Charles' Song - songsc@umich.edu

<span style="color:grey"> MS Student, School of Information, University of Michigan. </span>

This is my course project of SI 618: Data Manipulation and Analysis.

## Acknowledgement

The NHC crawler code is originally from 机灵鹤(2021),[Python网络爬虫实战：爬取卫健委官网文章](https://juejin.cn/post/6996985734854869000)
