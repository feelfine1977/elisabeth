import pandas as pd
import pm4py
import json
import numpy as np

def import_csv(file_path):
    event_log = pd.read_csv(file_path, sep=',')
    event_log = pm4py.format_dataframe(event_log, case_id='case_id', activity_key='event', timestamp_key='timestamp')
    start_activities = pm4py.get_start_activities(event_log)
    end_activities = pm4py.get_end_activities(event_log)
    print("Start activities: {}\nEnd activities: {}".format(start_activities, end_activities))
    return event_log

def get_model(log, model_type="bpmn"):
    if model_type == "process_tree":
        model = pm4py.discover_tree_inductive(log)
        pm4py.view_process_tree(model)
    elif model_type == "dfg":
        model, start_activities, end_activities = pm4py.discover_dfg(log)
        pm4py.view_dfg(model, start_activities, end_activities)
    elif model_type == "heuristic_net":
        model = pm4py.discover_heuristics_net(log)
        pm4py.view_heuristics_net(model)
    elif model_type == "bpmn":
        tree = pm4py.discover_tree_inductive(log)
        model = pm4py.convert_to_bpmn(tree)
        pm4py.view_bpmn(model)
    else :
        print("Model type not supported")
        return None
    return model
    


def process_event_log(file_path):
    # Read the event log from CSV file
    event_log = pd.read_csv(file_path)
    
    # Convert the DataFrame to a PM4Py Event Log object
    #event_log = pm4py.objects.log.conversion.dataframe.from_dataframe(event_log)
    
    # Perform some analysis on the event log
    net, im, fm = pm4py.discover_petri_net_inductive(event_log, activity_key='concept:name', case_id_key='case:concept:name', timestamp_key='time:timestamp')

    
    # Return the result
    return net, im, fm

def get_statistics(log, file_output="statistics.json"):
    event_log = pm4py.format_dataframe(log, case_id='case_id', activity_key='event', timestamp_key='timestamp')
    result = {}
    start_activities= pm4py.stats.get_start_activities(log)
    end_activities = pm4py.stats.get_end_activities(log)
    event_attributes = pm4py.stats.get_event_attributes(log)
    trace_attributes = pm4py.stats.get_trace_attributes(log)
    event_attribute_values = pm4py.stats.get_event_attribute_values(event_log,'concept:name')
    trace_attribute_values = pm4py.stats.get_trace_attribute_values(event_log,'concept:name')
    variants = pm4py.stats.get_variants(log)
    case_arrival_average = pm4py.stats.get_case_arrival_average(log)
    cycle_time = pm4py.stats.get_cycle_time(log)
    all_case_duration = pm4py.stats.get_all_case_durations(log)
    #case_duration = pm4py.stats.get_case_duration(event_log, case_id = 'case:concept:name')
    #stochastic_language = pm4py.stats.get_stochastic_language(log)
    
    result['start_activities'] = {k: int(v) for k, v in start_activities.items()}
    result['end_activities'] = {k: int(v) for k, v in end_activities.items()}
    result['event_attributes'] = event_attributes
    result['trace_attributes'] = trace_attributes
    result['event_attribute_values'] = {k: int(v) for k, v in event_attribute_values.items()}
    result['trace_attribute_values'] = {k: int(v) for k, v in trace_attribute_values.items()}
    result['variants'] = {k: int(v) for k, v in variants.items()}
    result['case_arrival_average'] = int(case_arrival_average)
    result['cycle_time'] = int(cycle_time)
    result['all_case_duration'] = [value for value in all_case_duration]
    #result['case_duration'] = {k: int(v) for k, v in case_duration.items()}
    #result['stochastic_language'] = {k: int(v) for k, v in stochastic_language.items()}
    
    print(result)
    
    with open(file_output, "w") as f:
        json.dump({"statistics": result}, f)
    
    return result

    
    

file_path = "/Users/urszulajessen/Documents/GitHub/elisabeth/src/eventlog.csv"
event_log = import_csv(file_path)
results = get_statistics(event_log)