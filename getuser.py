from config import *

#
# Fetch basic account information
#

r = requests.get(
	url     = "{}/{}".format(SANDBOX_URL,PROFILE_ENDPOINT),
	params  = {},
	headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'}
);

#
# Convert the JSON into a 1 row dataframe containing account information
#

df_profile = pd.json_normalize(r.json()['profile']);

print("PROFILE");
print(df_profile);