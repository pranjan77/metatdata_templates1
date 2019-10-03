/*
   A KBase module: metadata_templates
 */




module metadata_templates {


  typedef structure {
    string sample_template;
    string additional_sample_fields;
  } input;


  typedef structure {
    string report_name;
    string report_ref;
  } ReportResults;

  /*
     This example function accepts any number of parameters and returns results in a KBaseReport
   */
  funcdef run_metadata_templates(input params) returns (ReportResults output) authentication required;

};
