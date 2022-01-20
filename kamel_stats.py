import pyracing.client
import asyncio
import sys

username = sys.argv[1]
password = sys.argv[2]

ir = pyracing.client.Client(username, password)

data_to_print = []
driver_data_per_season = []

async def main():

    list_of_season_objects = await ir.current_seasons(only_active=False)

    for season in list_of_season_objects:
        #hardcoded to look for Kamel GT
        if season.series_id == 285:
            drivers_per_season = []
            #print(season.season_id)
            #for car_class in season.car_classes:
            #    print(f'{car_class.id}')
            print(f'\nSchedule for {season.series_name_short}' 
                    f' ({season.season_year} S{season.season_quarter})')
            
            for t in season.tracks:
                print(f'    Week {t.race_week} will take place at {t.name} ({t.config})')
                drivers = []
                list_race_result = await ir.series_race_results(season.season_id, race_week=(t.race_week+1))
                for race in list_race_result:
                    try:
                        subsession_data = await ir.subsession_data(subsession_id=race.subsession_id)
                        #print(f'{subsession_data.time_start} : {race.subsession_id} : {len(subsession_data.drivers)}')
                        for driver in subsession_data.drivers:
                            #print(f'{driver.display_name}')
                            drivers.append(driver.display_name)
                            drivers_per_season.append(driver.display_name)
                    except Exception as err:
                        print(f'Weird error on {race.subsession_id} + {err}')
                print(len(list(set(drivers))))
                print(list(set(drivers)))
                data_to_print.append([season.series_name_short, str(season.season_year), str(season.season_quarter),
                                      str(t.race_week + 1), t.name, t.config, str(len(list(set(drivers))))])
            driver_data_per_season.append([season.series_name_short, str(season.season_year), str(season.season_quarter),
                                           str(len(list(set(drivers_per_season))))])
    with open('kamel_weeks.csv', 'w') as f:
        f.write("Series,Year,Season,Week,Location,Config,Unique Drivers\n")
        for data in data_to_print:
            f.write(",".join(data))
            f.write("\n")

            
    with open('kamel_seasons.csv', 'w') as f:
        f.write("Series,Year,Season,Unique Drivers\n")
        for data in driver_data_per_season:
            f.write(",".join(data))
            f.write("\n")

asyncio.run(main())
