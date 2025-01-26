import json
import os
import re
import subprocess

# Define paths
repo_dir = "."
config_path = os.path.join(repo_dir, "config.json")
default_config_path = os.path.join(repo_dir, "default_config.json")


def merge_configs():
	"""Merge the existing config with the default config schema."""
	try:
		with open(default_config_path, "r") as default_file:
			default_config = json.load(default_file)

		if os.path.exists(config_path):
			with open(config_path, "r") as user_file:
				user_config = json.load(user_file)
		else:
			user_config = {}

		# Merge: Keep user's values where they exist, otherwise use defaults
		updated_config = {key: user_config.get(key, default_config[key]) for key in default_config}

		# Save the updated config
		with open(config_path, "w+") as config_file:
			json.dump(updated_config, config_file, indent=4)

		print("Configuration updated to the latest schema.")
	except Exception as e:
		print(f"Error while updating config: {e}")


def deploy_app():
	"""Pull the latest release, update config, install dependencies, and restart the app."""
	with open(config_path, "r") as f:
		config = json.load(f)

	try:
		# Fetch all tags (releases)
		subprocess.run(["git", "fetch", "--tags"], check=True, cwd=repo_dir)

		# Get the latest release tag (assuming it follows semantic versioning)
		result = subprocess.run(["git", "tag", "-l"], capture_output=True, text=True, cwd=repo_dir)
		tags = result.stdout.strip().split("\n")

		if not tags:
			print("No tags found in the repository.")
			return

		latest_tag = sorted(tags, reverse=True)[0]  # Get the latest tag

		if not latest_tag:
			print("No valid tags found.")
			return

		print(f"Deploying version: {latest_tag}")

		# Checkout the latest release tag
		checkout = subprocess.run(["git", "checkout", latest_tag], check=True, cwd=repo_dir)

		# Update configuration
		merge_configs()

		# Install dependencies
		subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True, cwd=repo_dir)

		# Restart the service
		if len(list(re.findall("Already", checkout.stdout))) < 1:
			try:
				subprocess.run(["sudo", "systemctl", "restart", "Raccoon-Dash"], check=True)
			except subprocess.CalledProcessError:
				print(
					"Systemctl failed to restart the service. Make sure it is running. If you're not on Linux, ignore this message.")

		print(f"Deployment to version {latest_tag} completed successfully!")
	except subprocess.CalledProcessError as e:
		print(f"Deployment failed: {e}")


if __name__ == "__main__":
	deploy_app()
