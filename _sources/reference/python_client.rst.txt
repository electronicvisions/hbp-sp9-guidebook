=======================
Python client reference
=======================

.. currentmodule:: nmpi


.. autoclass:: Client

   .. attribute:: user_info

      Information about the current user, as retrieved from the Collaboratory
   
   .. automethod:: submit_job
   .. automethod:: job_status
   .. automethod:: get_job
   .. automethod:: remove_completed_job
   .. automethod:: remove_queued_job
   .. automethod:: queued_jobs
   .. automethod:: completed_jobs
   .. automethod:: download_data
   .. automethod:: copy_data_to_storage
   .. automethod:: create_data_item
   .. automethod:: create_resource_request
   .. automethod:: edit_resource_request
   .. automethod:: list_resource_requests
   .. automethod:: list_quotas
   .. automethod:: my_collabs
