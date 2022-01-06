// Can you tell I mainly program in C/C++?

function autofill_api_data(){

    // get data in order
    const cururl = window.location;
    const params = "apikey=89fd5dac86c45394636508a826bdda";
    const url = cururl.protocol + "//" + cururl.host + "/api/all.json?canary=" + covid_api_canary;

    // make new request, format, and send
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "json";
    xhr.send();

    // define callback
    xhr.onreadystatechange=(e)=>{

        // only process when done
        if (xhr.readyState === XMLHttpRequest.DONE) {

            // if bad, alert.
            if (xhr.status != 200){
                alert(
                    "Error while getting data from API! ("+xhr.status+")\n"+
                    "See console for more info!"
                );
                console.log(xhr.response);
                return;
            }

            // hand off to formatting func
            fill_data(xhr.response);

            // hide loading, show data
            document.getElementById("loading").style.display = "none";
            document.getElementById("content").style.display = "block";
        
        }
    }
}

function fill_data(data){

    // if data is empty, return
    if (data == null) return 1;

    // start with fsu reported cases
    document.getElementById('fsu.new_cases').innerHTML = data['fsu.reported_cases']['new_cases'];
    document.getElementById('fsu.total_cases').innerHTML = data['fsu.reported_cases']['total'];
    document.getElementById('fsu.rc_last_updated').innerHTML = data['fsu.reported_cases']['last_updated'];

    // fsu estimated cases
    document.getElementById('fsu.population').innerHTML = data['fsu.estimates']['population']['total'];
    document.getElementById('fsu.pop_year').innerHTML = data['fsu.estimates']['population']['year'];
    document.getElementById('fsu.pos_rate').innerHTML = data['fsu.estimates']['positivity_rate']*100;
    document.getElementById('fsu.stu_pos').innerHTML = data['fsu.estimates']['students']['positive'];
    document.getElementById('fsu.stu_cc').innerHTML = data['fsu.estimates']['students']['close_contacts'];
    document.getElementById('fsu.empl_pos').innerHTML = data['fsu.estimates']['employees']['positive'];
    document.getElementById('fsu.empl_cc').innerHTML = data['fsu.estimates']['employees']['close_contacts'];
    document.getElementById('fsu.est_last_updated').innerHTML = data['fsu.estimates']['last_updated'];

    // fsu testing
    document.getElementById('fsu.tst_start').innerHTML = data['fsu.testing']['start'];
    document.getElementById('fsu.tst_end').innerHTML = data['fsu.testing']['end'];
    document.getElementById('fsu.tests_given').innerHTML = data['fsu.testing']['total_tests'];
    document.getElementById('fsu.test_stu_pos').innerHTML = data['fsu.testing']['students']['positive'];
    document.getElementById('fsu.test_empl_pos').innerHTML = data['fsu.testing']['employees']['positive'];
    document.getElementById('fsu.test_pos_rate').innerHTML = data['fsu.testing']['positivity_rate'];

    // leon metrics
    document.getElementById('leon.pos_rate').innerHTML = data['leon.metrics']['positivity_rate']*100;
    document.getElementById('leon.vac_ratio').innerHTML = data['leon.metrics']['vaccination_ratio']*100;
    document.getElementById('leon.cases_per_100k').innerHTML = data['leon.metrics']['cases_per_100k'];
    document.getElementById('leon.r_naught').innerHTML = data['leon.metrics']['r_naught'];
    document.getElementById('leon.r_naught_ci90').innerHTML = data['leon.metrics']['r_naught_ci90'];
    document.getElementById('leon.met_last_updated').innerHTML = data['leon.metrics']['last_updated'];

    // leon actuals
    document.getElementById('leon.new_cases').innerHTML = data['leon.actuals']['new_cases'];
    document.getElementById('leon.total_cases').innerHTML = data['leon.actuals']['total_cases'];
    document.getElementById('leon.new_deaths').innerHTML = data['leon.actuals']['new_deaths'];
    document.getElementById('leon.total_deaths').innerHTML = data['leon.actuals']['total_deaths'];
    document.getElementById('leon.vac_count').innerHTML = data['leon.actuals']['vac_count'];
    document.getElementById('leon.act_last_updated').innerHTML = data['leon.actuals']['last_updated'];
    
    // return
    return 0;
}