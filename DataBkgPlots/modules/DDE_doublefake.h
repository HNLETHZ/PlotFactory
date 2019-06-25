// This namespace prepares the doublefakerate measured via DDE.py to be implementable in dataframe for the main plotting tool.
// Run the following once before using the namespace: gROOT->ProcessLine(".L modules/DDE_doublefake.h+");
namespace dfr_namespace {
	double getDoubleFakeRate(double ptCone, double eta, double dr12, double displacement){
		if (displacement >= 0.0 && displacement < 0.3) {
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.041237;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.102941;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.008197;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.023438;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.030928;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.015267;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.011321;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.005348;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.004292;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.000000;
			return 0.;
		}
		if (displacement >= 0.3 && displacement < 10.0) {
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.018868;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 10.000000 && ptCone < 20.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.071429;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.006849;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 20.000000 && ptCone < 30.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.038462;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.015000;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 30.000000 && ptCone < 40.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.030928;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.005236;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 40.000000 && ptCone < 70.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.016279;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 0.000000 && eta < 1.200000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.001637;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.000000 && dr12 < 0.050000) return 0.000000;
			if (ptCone >= 70.000000 && ptCone < 2000.000000 && eta >= 1.200000 && eta < 2.400000 && dr12 >= 0.050000 && dr12 < 1.000000) return 0.002257;
			return 0.;
		}
		return 0.;
	}
}
