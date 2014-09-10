help:
	@echo "clean - remove build artifacts"
	@echo "run - run the local development server for testing/debugging purposes"
	@echo "test - run all of the app's tests and print a coverage report"

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -empty -type d -delete

deploy: clean
	# deploy application to the default environment
	appcfg.py update .                                                  \
		--oauth2                                                        \
		--oauth2_credential_file=/.appengine_storage/deploy_credentials \
		--noauth_local_webserver                                        \
		-A $(app)                                                       \
		-V $(version)                                                   \

run: clean
	# run the appengine development server
	dev_appserver.py .                            \
		--host 0.0.0.0                            \
		--admin_host 0.0.0.0                      \
		--datastore_consistency_policy consistent \
		--storage_path /.appengine_storage/       \
		--skip_sdk_update_check

test: clean
	@python tests/run-tests.py
