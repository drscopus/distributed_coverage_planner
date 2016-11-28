import min_alt_discrt as discrt
import get_mapping
import dubins_cost
import solver
import greedy_decompose
import adjacency
import coverage_plot as splot
import min_alt_decompose



GLKH_LOCATION = "/home/sbochkar/misc/GLKH-1.0/"


def single_planner(decomp, radius=1.0, orig_poly=[]):
	"""
	Single agent path planner:
	"""

	single_decomposition_list = []
	adj_matrix_list = []
	segment_list = []
	map_list = []
	tours = []
	for region in decomp:

		#single_decomp = greedy_decompose.decompose(region)
		#single_decomp = min_alt_decompose.decompose(region)
		single_decomposition_list.append(min_alt_decompose.decompose(region))
		#adjacency_matrix = adjacency.get_adjacency_as_matrix(single_decomposition_list[-1])
		adj_matrix_list.append(adjacency.get_adjacency_as_matrix(single_decomposition_list[-1]))


		#segments = discrt.discritize_set(single_decomp, radius)
		segment_list.append( discrt.discritize_set(single_decomposition_list[-1], radius))
		#mapping = get_mapping.get_mapping(segments)
		map_list.append(get_mapping.get_mapping(segment_list[-1]))
		cost_matrix, cluster_list = dubins_cost.compute_costs(region, map_list[-1], radius/2)
		solver.solve("cpp_test", GLKH_LOCATION, cost_matrix, cluster_list)
		#tour = solver.read_tour("cpp_test")
		tours.append(solver.read_tour("cpp_test"))

	#Initialize plotting tools
	ax = splot.init_axis()
	for idx, region in enumerate(decomp):
		splot.plot_polygon_outline(ax, region, idx)
		splot.plot_decomposition(ax, single_decomposition_list[idx], adj_matrix_list[idx], region)
		splot.plot_samples(ax, segment_list[idx])
		#splot.plot_init_poss_and_assignment(ax, sites, cell_to_site_map, decomp)
		splot.plot_tour_dubins(ax, tours[idx], map_list[idx], radius/2)
	splot.display()


	return []