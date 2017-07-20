============================
How to write a Custom Action
============================

1. Write a class inherited from mistral.actions.Action

 .. code-block:: python

    from mistral_lib import actions

    class RunnerAction(actions.Action):
        def __init__(self, param):
            # store the incoming params
            self.param = param

        def run(self, context):

            # Actions can be returned in a manner of ways. The simplest is
            # return {'status': 0}
            # or using a Result object. The Result has an optional parameter data
            # that can be used to transfer information
            return actions.Result()
            # Failed executions can also be returned using a workflow Result object
            # that contains an non empty error parameter such as:
            # return actions.Result(error="error text")


2. Publish the class in a namespace (in your ``setup.cfg``)


 .. code-block:: ini

   [entry_points]
   mistral.actions =
       example.runner = my.mistral_plugins.somefile:RunnerAction

3. Reinstall your library package if it was installed in system (not in virtualenv).

4. Run db-sync tool to ensure your actions are in Mistral's database

 .. code-block:: console

    $ mistral-db-manage --config-file <path-to-config> populate

5. Now you can call the action ``example.runner``

  .. code-block:: yaml

    my_workflow:
      tasks:
        my_action_task:
          action: example.runner
          input:
            param: avalue_to_pass_in
