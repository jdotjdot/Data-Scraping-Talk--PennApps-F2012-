# Runs our scraper indefinitely
# will only stop upon a GRACEFUL exit--
#  but keep in mind a graceful exit only means that
#  no error is thrown, but that doesn't mean that we
#  actually want the program to end!

until python scraper.py; do
	echo "Process crashed with exit code $?.  Respawning..." >&2
	sleep 2
done
