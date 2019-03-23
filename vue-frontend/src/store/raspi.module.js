import ApiService from "../common/api.service";
import { REBOOT } from "./actions.type";

const actions = {
  [REBOOT]() {
    return new Promise(( resolve, reject ) => {
      ApiService.post("raspi/reboot")
    });
  }
}

export default {
  actions
};
