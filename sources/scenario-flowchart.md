# Scenario Graph Reference

Searchable scenario graph for campaign thread tracking.

Scenario names come from `sources/extracted/scenario-index.md`.

Notes:

- "Leads to" records outgoing scenario-to-scenario links. Treat these as graph links, not a complete rules reference for unlock requirements.
- This file records the scenario graph and storyline only. It does not track locked links, forced immediate links, sticker requirements, or other special unlock conditions.

## Storyline Legend

| Storyline |
| --- |
| Introduction |
| Algox |
| Lurker |
| Unfettered |
| Puzzle Book |
| Personal Quest |
| Job Posting |
| Random Scenario |
| Other |

## Scenario Graph

| Scenario | Title                              | Storyline       | Leads to   |
| -------- | ---------------------------------- | --------------- | ---------- |
| 0        | Howling in the Snow                | Introduction    | None shown |
| 1        | A Town in Flames                   | Introduction    | 2, 3       |
| 2        | Algox Scouting                     | Introduction    | 4          |
| 3        | Algox Offensive                    | Introduction    | 4          |
| 4        | Heart of Ice                       | Introduction    | 5, 6, 7, 8 |
| 5        | Frozen Crypt                       | Algox           | 9, 10      |
| 6        | Avalanche                          | Algox           | 11, 12     |
| 7        | Edge of the World                  | Lurker          | 13, 14     |
| 8        | Crystal Trench                     | Unfettered      | 15, 16     |
| 9        | Glowing Catacombs                  | Algox           | 17         |
| 10       | Crystal Enclosure                  | Algox           | 18         |
| 11       | Snowscorn Peak                     | Algox           | 19         |
| 12       | Temple Entrance                    | Algox           | 20         |
| 13       | Frozen Fjord                       | Lurker          | 21, 32     |
| 14       | Jagged Shoals                      | Lurker          | 22         |
| 15       | Ancient Spire                      | Unfettered      | 23, 24     |
| 16       | Derelict Elevator                  | Unfettered      | 23, 26     |
| 17       | Haunted Vault                      | Algox           | 27, 56     |
| 18       | Crystal Fields                     | Algox           | 29         |
| 19       | Skyhall                            | Algox           | 28, 30     |
| 20       | Temple of Liberation               | Algox           | 31         |
| 21       | Realm of Endless Frost             | Lurker          | None shown |
| 22       | Ice Floes                          | Lurker          | 33         |
| 23       | Spire Basement                     | Unfettered      | 34         |
| 24       | Upper Spire                        | Unfettered      | 34         |
| 25       | Rusted Tunnels                     | Unfettered      | 35         |
| 26       | Quatryl Library                    | Unfettered      | 36         |
| 27       | Depths of Delirium Shard Seeker    | Algox           | None shown |
| 28       | Summit Meeting                     | Algox           | 38         |
| 29       | War of the Spire A                 | Algox           | 39         |
| 30       | War of the Spire B                 | Algox           | 40         |
| 31       | Crackling Tunnel                   | Algox           | 41         |
| 32       | Ravens' Roost                      | Lurker          | None shown |
| 33       | Thawed Wood Into the Forest        | Lurker          | 42, 50     |
| 34       | Top of the Spire                   | Unfettered      | None shown |
| 35       | Scrap Pit                          | Unfettered      | 43         |
| 36       | Buried Ducts                       | Unfettered      | 44         |
| 37       | The Dead Mile                      | Unfettered      | 44         |
| 38       | The Way Forward                    | Algox           | 45, 46     |
| 39       | Corrupted Camp Into the Forest     | Algox           | 47         |
| 40       | Relief Effort                      | Algox           | 48         |
| 41       | Unfettered Shard Shard Seeker      | Algox           | None shown |
| 42       | Sunless Trench                     | Lurker          | 49         |
| 43       | Overrun Barricade                  | Unfettered      | 51         |
| 44       | Nerve Center                       | Unfettered      | 58, 59     |
| 45       | Living Glacier                     | Algox           | 52         |
| 46       | Dead Pass                          | Algox           | None shown |
| 47       | Carrion Ridge                      | Algox           | 56         |
| 48       | Blizzard Island                    | Algox           | 57         |
| 49       | Beneath Sea and Stone              | Lurker          | 53         |
| 50       | Explosive Descent                  | Lurker          | 54         |
| 51       | Orphan's Halls                     | Unfettered      | 58, 59     |
| 52       | Fleeting Permanence                | Algox           | 55         |
| 53       | Underwater Throne                  | Lurker          | 60         |
| 54       | Among the Wreckage                 | Lurker          | 60         |
| 55       | Change of Heart                    | Algox           | None shown |
| 56       | Call of the Harbinger              | Algox           | None shown |
| 57       | Sanctuary of Snow                  | Algox           | None shown |
| 58       | Orphan's Core                      | Unfettered      | None shown |
| 59       | Automaton Uprising                 | Unfettered      | None shown |
| 60       | Uniting the Crown                  | Lurker          | None shown |
| 61       | Life and Death                     | Puzzle Book     | 62         |
| 62       | The Unfettered Seal                | Puzzle Book     | 63         |
| 63       | The Savvas Seal                    | Puzzle Book     | 64         |
| 64       | The Frosthaven Seal                | Puzzle Book     | None shown |
| 65       | A Strong Foundation                | Personal Quest  | 66         |
| 66       | Elemental Cores                    | Personal Quest  | 67         |
| 67       | Core Attunement                    | Personal Quest  | 68         |
| 68       | The Face of Torment                | Personal Quest  | None shown |
| 69       | Sacred Soil Into the Forest        | Personal Quest  | 70         |
| 70       | The True Oak                       | Personal Quest  | None shown |
| 71       | Invasion of the Dock               | Personal Quest  | 72         |
| 72       | A Giant Block of Ice               | Personal Quest  | 73         |
| 73       | Flotsam                            | Personal Quest  | 74, 75     |
| 74       | Gaps in the Road                   | Personal Quest  | 76         |
| 75       | Infiltrating the Lair              | Personal Quest  | 77         |
| 76       | Apotheosis                         | Personal Quest  | 77         |
| 77       | Fish King's Ascension              | Personal Quest  | None shown |
| 78       | The Lurker Problem                 | Job Posting     | None shown |
| 79       | Relic                              | Job Posting     | 80         |
| 80       | Relic Renewed                      | Job Posting     | None shown |
| 81       | Ruinous Research Lab               | Other           | None shown |
| 82       | Expedition North                   | Other           | None shown |
| 83       | Rising Brine                       | Job Posting     | None shown |
| 84       | Here There Be Oozes                | Job Posting     | None shown |
| 85       | Deadly Pastimes                    | Job Posting     | None shown |
| 86       | The Lady in White                  | Job Posting     | 90         |
| 87       | The Collection                     | Job Posting     | 88         |
| 88       | Collection's Capstone              | Job Posting     | None shown |
| 89       | A Contained Fire                   | Job Posting     | None shown |
| 90       | Frozen Treasure                    | Job Posting     | 91         |
| 91       | Shoreline Scramble                 | Job Posting     | None shown |
| 92       | Sinking Ship                       | Job Posting     | None shown |
| 93       | Midwinter Brawl                    | Job Posting     | None shown |
| 94       | A Grand View                       | Job Posting     | 95         |
| 95       | To Bury the Dead                   | Job Posting     | None shown |
| 96       | Underground Station                | Job Posting     | 97         |
| 97       | Program Control Nexus              | Job Posting     | 98         |
| 98       | Collapsing Vent                    | Job Posting     | None shown |
| 99       | Prison Break                       | Job Posting     | 100        |
| 100      | Inside the Swarm                   | Job Posting     | 101        |
| 101      | Harrower Library Into the Forest   | Job Posting     | 102        |
| 102      | Into the Black                     | Job Posting     | 103        |
| 103      | The Lead Door                      | Job Posting     | None shown |
| 104      | Ruins of the Solstice              | Random Scenario | 105, 106   |
| 105      | Ruins of the Equinox               | Random Scenario | None shown |
| 106      | The Tempus Forge                   | Random Scenario | None shown |
| 107      | My Private Empire                  | Random Scenario | None shown |
| 108      | Lustrous Pit                       | Random Scenario | None shown |
| 109      | Furious Factory                    | Random Scenario | None shown |
| 110      | Guardian's Temple                  | Random Scenario | None shown |
| 111      | Ice Cave                           | Other           | None shown |
| 112      | Raised by Wolves                   | Other           | None shown |
| 113      | Lush Grotto                        | Other           | None shown |
| 114      | Work Freeze                        | Other           | 115        |
| 115      | Pylon Problems                     | Other           | 116        |
| 116      | Caravan Guards                     | Other           | None shown |
| 117      | A Waiting Game                     | Other           | None shown |
| 118      | Lurker Necromancy                  | Other           | None shown |
| 119      | Radiant Dust Into the Forest       | Other           | None shown |
| 120      | Under the Influence                | Other           | 121        |
| 121      | Black Memories                     | Other           | None shown |
| 122      | The Eternal Crave                  | Other           | None shown |
| 123      | The Titan                          | Other           | None shown |
| 124      | A Growing Problem                  | Other           | 125        |
| 125      | The Longest Second                 | Other           | None shown |
| 126      | Joseph the Lion                    | Other           | None shown |
| 127      | Derelict Freighter                 | Other           | None shown |
| 128      | A Tall Drunken Tale                | Other           | 129        |
| 129      | How to Lay an Ambush               | Other           | 130        |
| 130      | And Then, a Stream                 | Other           | None shown |
| 131      | The Dancing Iceberg                | Other           | None shown |
| 132      | Temple of Feline Power             | Job Posting     | 133        |
| 133      | Bolt                               | Job Posting     | None shown |
| 134      | Tower of Knowledge Into the Forest | Other           | None shown |
| 135      | Belara's Keep                      | Other           | None shown |
| 136      | Abandoned Hideout                  | Other           | None shown |
| 137      | Pirate Queen's Haul                | Other           | None shown |
