featureform deploy docker --quickstart
export FEATUREFORM_HOST=localhost:7878
featureform apply --insecure quickstart/definitions.py


# ---
sudo -u postgres psql transactions < dump_transactions.sql 
