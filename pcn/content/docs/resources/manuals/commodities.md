---
weight: 999
title: "Commodities"
description: ""
icon: "article"
date: "2025-04-05T18:03:35-05:00"
lastmod: "2025-04-05T18:03:35-05:00"
draft: false
toc: true
---
## What are commodities?

Commodities are the products of your industry. They are consumed by other industry, your populations, and your government. They are freely traded all around Enkon.


## How to register a product.

1. Give your commodity a name.
2. Select its Category (see below)
3. Type up a brief description.
4. Set your commodity to true or false. true means your commodity is global and can be produced by anyone. false means it is proprietary and only your nation can produce it or you can license it out.
5. Finally, type in your nation name in lowercase. If your nation has spaces (St Saratoga), type it like this st_saratoga.
```yaml
Product: #Nothing goes here
    Name: Tanks
    Category: ARMCON 
    Description: Armored beasts of war
    Global: true
    Origin: world
```
## List of Commodities
{{< commodities_list "assets/data/economy/commodities.yaml" >}}