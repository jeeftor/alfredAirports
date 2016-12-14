OUTPUT=$(python build/packageWorkflow.py . -o build/)
TEXT_ARRRAY=($OUTPUT)

echo ${TEXT_ARRRAY[0]}
echo ${TEXT_ARRRAY[1]}
echo ${TEXT_ARRRAY[2]}



# https://github.com/repos/jeeftor/alfredAirports/releases

# POST /repos/:owner/:repo/releases

# {
#   "tag_name": "v1.0.0",
#   "target_commitish": "master",
#   "name": "v1.0.0",
#   "body": "Description of the release",
#   "draft": false,
#   "prerelease": false
# }


