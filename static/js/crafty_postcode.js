// This enables UK postcode lookup using craftyclicks.co.uk
// It works with multiple addresses on a form
// 
// How to implement postcode lookup:
//      1) Set id of address fields to prefix + address1, address2, address3, town, county, postcode
//		2) Prefix can be blank but must be different for each address on same page e.g. bill_, ship_
//      3) In the table definition for the postcode field set widget=postcode
//      4) Test free using postcodes AA11AA, AA11AB, AA11AD or AA11AE
//      5) Buy credits from craftyclicks.co.uk and enter token below
//
function postcodeLookup(elem)
{
    var craftytoken="xxxxx-xxxxx-xxxxx-xxxxx"
    var crafty = CraftyPostcodeCreate();
    var prefix=elem.id.substr(0,elem.id.indexOf("postcode"));
	
	// assign output fields
    crafty.set("elem_street1"  , prefix+"address1");
    crafty.set("elem_street2"  , prefix+"address2");
    crafty.set("elem_street3"  , prefix+"address3");
    crafty.set("elem_town"     , prefix+"town");
    crafty.set("elem_county"   , prefix+"county");
    crafty.set("elem_postcode" , prefix+"postcode");
    crafty.set("result_elem_id", "postcode_results");

    // set options (http://www.craftyclicks.co.uk/web-service/docs/javascript-address-finder-user-guide)
    crafty.set("access_token", craftytoken);
    crafty.set("busy_img_url", "/");    // the default calls the host page controller
    crafty.set("single_res_autoselect" , 1); // automatically select if only one address found
    crafty.set("hide_result", "1"); // hide the results box once selection made
    message = "Postcode not found. If testing then try AA11AA, AA11AB, AA11AD or AA11AE"
    crafty.set("err_msg1", message)
    crafty.set("err_msg2", message)
    crafty.doLookup();
}
