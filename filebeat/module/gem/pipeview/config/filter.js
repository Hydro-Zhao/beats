var params = {cycle_time: 500};//try with yaml environment variable {{.cycle_time}}
function register(scriptParams) {
    params = scriptParams;
}
function process(event) {
    var lines = event.Get("message");
    var line = lines.split(/\n/);
    var inst = {};
    for (var i=0; i<lines.length; ++i) {
        var fields = line[i].split(/:\s*/);
        // TODO  here I do not count efficiency, these ifs can be cut off
        // be aware of that the time of the last event may not be "retire" if the instruction is not comlpeted.
        if (fields[0] == "O3PipeView") {
            if (fields[1] == "fetch") {
                inst["start_tick"] = Number(fields[2]);
                inst["end_tick"] = Number(fields[2]);

                inst["pc_upc"] = fields[3] + fields[4];
                inst["seq_num"] = Number(fields[5]);
                inst["disasm_instruction"] = fields[6];
                inst["disasm_assembly"] = fields[7];
            } else if (fields[1] == "decode") {
                if (fields[2] != 0) {
                    inst["fetch"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                }
            } else if (fields[1] == "rename") {
                if (fields[2] != 0) {
                    inst["decode"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                }
            } else if (fields[1] == "dispatch") {
                if (fields[2] != 0) {
                    inst["rename"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                }
            } else if (fields[1] == "issue") {
                // only can issue == dispatch(conclude from o3-pipeview.py)
                // maybe I can add a field to indicate this.
                if (fields[2] != 0) {
                    inst["dispatch"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                }
            } else if (fields[1] == "complete") {
                if (fields[2] != 0) {
                    inst["issue"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                }
            } else if (fields[1] == "retire") {
                // This will distinguish completed and abandoned intructions.
                if (fields[2] == 0) {
                    inst["abandoned_instuction"] = true;
                } else {
                    inst["abandoned_instuction"] = false;

                    inst["complete"] = Number(fields[2]) - inst["end_tick"];
                    inst["end_tick"] = Number(fields[2]);
                    // do not include store stage
                    //inst["end_tick"] = Number(fields[2]);// retire

                    // according to o3-pipeview.py, the width of the last stage will always be 1(*cycle-time), here, I assume that be 500
                    // however, I assume that the tick of store - the tick of retire is the tick spent on store
                    //inst["store"] = Number(fields[4]) - Number(fields[2]);
                    inst["store"] = Number(fields[4]);
                }
            }
        }
    }


    // insert to elasticsearch
    event.Put("gem5.pipeview.pc_upc" , inst["pc_upc"]);
    event.Put("gem5.pipeview.seq_num", inst["seq_num"]);
    event.Put("gem5.pipeview.disasm_instruction", inst["disasm_instruction"]);
    event.Put("gem5.pipeview.disasm_assembly", inst["disasm_assembly"]);

    event.Put("gem5.pipeview.start_tick", inst["start_tick"]);
    event.Put("gem5.pipeview.end_tick", inst["end_tick"]);

    event.Put("gem5.pipeview.fetch", inst["fetch"]);
    event.Put("gem5.pipeview.decode", inst["decode"]);
    event.Put("gem5.pipeview.rename", inst["rename"]);
    event.Put("gem5.pipeview.dispatch", inst["dispatch"]);
    event.Put("gem5.pipeview.issue", inst["issue"]);
    event.Put("gem5.pipeview.complete", inst["complete"]);
    event.Put("gem5.pipeview.store", inst["store"]);

    event.Put("gem5.pipeview.abandoned_instuction", inst["stages"]);
    event.Put("gem5.pipeview.abandoned_instuction", inst["stages"]);

    event.Delete("message");
}
