build_base:
	rm -f steam_base.csv
	rm -f sorted_output.csv
	rm -f scored_output.csv
	rm -f unique_scored_output.csv
	rm -f output.csv
	rm -f games_list.json
	./manage.py game_list_from_json --file ${BASE_FILE}
	./manage.py json_to_csv --file ${BASE_FILE} --cols steam_id,app_id,total_hours_played
	sort output.csv -t, -n -k1 > sorted_output.csv
	./manage.py score_csv --file sorted_output.csv
	sort -u scored_output.csv > unique_scored_output.csv
	sort unique_scored_output.csv -t, -n -k1 > steam_base.csv
	
