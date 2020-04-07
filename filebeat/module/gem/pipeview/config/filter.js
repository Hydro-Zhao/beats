//var params = {cycle_time: 1000};//try with yaml environment variable {{.cycle_time}}
//function register(scriptParams) {
//    params = scriptParams;
//}
function process(event) {
    //var StagesEnum = {
    //   "FETCH": 0,
    //    "DECODE": 1,
    //    "RENAME": 2,
    //    "DISPATCH": 3,
    //    "ISSUE": 4,
    //    "COMPLETE": 5,
    //    "RETIRE": 6,
    //    "STORE": 7
    //};

    var lines = event.Get("message");
    var line = lines.split(/\n/);
    var inst = {};
    inst["stages"] = [];
    for (var i=0; i<lines.length; ++i) {
        var fields = line[i].split(/:\s*/);

        // version 1
        //if (fields[0] == "O3PipeView") {
        //   inst["stages"].push({fields[1]: Number(fields[2])});
        //    if (fields[1] == "fetch") {
        //        inst["pc_upc"] = fields[3] + fields[4];
        //        inst["seq_num"] = Number(fields[5]);
        //        inst["disasm"] = fields[6];
        //        inst["start_tick"] = inst["fetch"];
        //    } else if (fields[1] == "retire") {// I am not sure whether the && is ... in javascript
        //        inst["stages"].push({fields[3]: Number(fields[4])});
        //        // This will distinguish completed and abandoned intructions.
        //        if (inst["stages"]["retire"] == 0) {
        //            inst["disasm.abandoned_instuction"] = true;
        //        } else {
        //            inst["disasm.abandoned_instuction"] = false;
        //        }
        //    }
        //}
        //
        // version 2
        // this is similar to the above if{}, it filts out stages whose tick is 0.
        if (fields[0] == "O3PipeView") {
            if (fields[1] != "retire"
            && fields[1] != "issue"
            && fields[2] != 0) {
                inst["stages"].push({fields[1]: Number(fields[2])});
                if (fields[1] == "fetch") {
                    inst["pc_upc"] = fields[3] + fields[4];
                    inst["seq_num"] = Number(fields[5]);
                    inst["disasm"] = fields[6];
                }
            } else if (fields[1] == "retire") {// I am not sure whether the && is ... in javascript
                inst["stages"].push({fields[1]: Number(fields[2])});
                inst["stages"].push({fields[3]: Number(fields[4])});
                // This will distinguish completed and abandoned intructions.
                if (inst["stages"]["retire"] == 0) {
                    inst["disasm.abandoned_instuction"] = true;
                } else {
                    inst["disasm.abandoned_instuction"] = false;
                }
            } else if (fields[1] == "issue") {
                if (inst["stages"][inst["stages"].length-1][0] == "dispatch"
                && inst["stages"][inst["stages"].length-1][1] == fields[2]) {
                    inst["stages"].pop();
                }
                if (fields[2] != 0) {
                    inst["stages"].push({fields[1]: Number(fields[2])});
                }
            }

        }
    }
    // TODO
    inst["stages"].sort(function(first, second) {return second[1] - first[1];});

    // Find out the time of the last event - it may not be "retire" if the instruction is not comlpeted.
    var len = inst["stages"].length
    var last_event_time = -Infinity;
    while (len--) {
        if (inst["stages"][len][1] > max) {
            last_event_time = inst["stages"][len][1];
        }
    }
    //according to o3-pipeview.py, the width of the last stage will always be 1(*cycle-time), here, I assume that be 500
    inst["stages"]["dum_stage"] = last_event_time + 500;

    // timestamps:
    // fetch is start_tick
    // dum_stage is end_tick

    // insert to elasticsearch
    event.Put("gem5.pipeview.pc_upc" , inst["pc_upc"]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
    event.Put("", inst[""]);
}
