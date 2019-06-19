// This namespace prepares the doublefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.
namespace dfr_namespace {
	double getDoubleFakeRate(double ptCone, double eta){
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 0.800000) return 0.018519;
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.800000 && eta < 1.200000) return 0.045455;
		if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.400000) return 0.073593;
		if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.000000 && eta < 0.800000) return 0.007576;
		if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.800000 && eta < 1.200000) return 0.045872;
		if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 1.200000 && eta < 2.400000) return 0.039216;
		if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.000000 && eta < 0.800000) return 0.025974;
		if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.800000 && eta < 1.200000) return 0.018692;
		if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 1.200000 && eta < 2.400000) return 0.034707;
		if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 0.800000) return 0.011173;
		if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.800000 && eta < 1.200000) return 0.008646;
		if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.400000) return 0.011152;
		if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.000000 && eta < 0.800000) return 0.002453;
		if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.800000 && eta < 1.200000) return 0.001942;
		if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 1.200000 && eta < 2.400000) return 0.001881;
		return 0.;
	}
}
