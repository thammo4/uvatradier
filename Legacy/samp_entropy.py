from itertools import combinations
from math import log
from config import *

def construct_templates(timeseries_data:list, m:int=2):
	'''
		Construct templates from the given time series data.

		Args:
			timeseries_data (list): The input time series data as a list of numerical data points.
			m (int): The embedding dimension, representing the length of templates. Default is 2.

		Returns:
			list: A list of templates extracted from the time series data.

	'''

	num_windows = len(timeseries_data) - m + 1
	return [timeseries_data[x:x+m] for x in range(0, num_windows)]


def get_matches(templates:list, r:float):
	'''
		Count the number of template matches based on the given tolerance parameter.

		Args:
			templates (list): A list of templates to compare.
			r (float): The tolerance parameter that defines the maximum difference allowed between data points of two templates to consider them as a match.

		Returns:
			int: The number of template matches.

	'''

	return len(list(filter(lambda x: is_match(x[0], x[1], r), combinations(templates, 2))))


def is_match(template_1:list, template_2:list, r:float):
	'''
		Check if two templates are a match within the given tolerance.

		Args:
			template_1 (list): The first template.
			template_2 (list): The second template.
			r (float): The tolerance parameter that defines the maximum difference allowed between data points of the two templates to consider them as a match.

		Returns:
			bool: True if the templates are a match, False otherwise.

	'''

	return all([abs(x - y) < r for (x, y) in zip(template_1, template_2)])


def sample_entropy(timeseries_data:list, window_size:int, r:float):
	'''
		Calculate the Sample Entropy of the given time series data.
		Sample Entropy quantifies the irregularity or complexity of a time series.

		Args:
			timeseries_data (list): The input time series data as a list of numerical data points.
			window_size (int): The embedding dimension, representing the length of templates.
			r (float): The tolerance parameter that defines the maximum difference allowed between data points of two templates to consider them as a match.

		Returns:
			float: The calculated Sample Entropy value.

	'''

	B = get_matches(construct_templates(timeseries_data, window_size), r)
	A = get_matches(construct_templates(timeseries_data, window_size+1), r);
	return -log(A/B);