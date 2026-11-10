from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import logging

# 1. 导入你刚刚打包的独立库 (包名是你设置的 RMB261)
import RMB261

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2. 初始化 MATLAB Runtime (只在启动时执行一次)
logging.info("正在初始化 MATLAB Runtime，请稍候...")
model = RMB261.initialize()
logging.info("MATLAB Runtime 初始化成功，API 服务准备就绪。")

@app.route('/run_matlab', methods=['GET', 'POST'])
def get_knowledge_graph_data():
    try:
        # 3. 调用函数并接收 10 个返回值
        # 注意：这里的函数名也是 RMB261，因为你的源文件叫 RMB261.m
        res = model.RMB261(nargout=10)

        # 4. 解析返回值 (严格按照 .m 文件的输出顺序)
        support_typ = np.array(res[0]).tolist()
        support_ice = np.array(res[1]).tolist()
        support_hea = np.array(res[2]).tolist()

        proto_typ = np.array(res[3])[0].tolist()
        proto_ice = np.array(res[4])[0].tolist()
        proto_hea = np.array(res[5])[0].tolist()

        traj_x = np.array(res[6])[0].tolist()
        traj_y = np.array(res[7])[0].tolist()
        dynamic_trajectory = [[x, y] for x, y in zip(traj_x, traj_y)]

        n_shots = int(res[8])
        n_steps = int(res[9])

        # 5. 构建并返回 JSON (保持不变)
        frontend_payload = {
            "status": "success",
            "message": "Dynamic knowledge base updated successfully",
            "data": {
                "spatial_features": {
                    "support_sets": {
                        "typhoon": support_typ,
                        "ice_storm": support_ice,
                        "heatwave": support_hea
                    },
                    "prototypes": {
                        "typhoon": proto_typ,
                        "ice_storm": proto_ice,
                        "heatwave": proto_hea
                    },
                    "dynamic_trajectory": dynamic_trajectory
                },
                "statistical_composition": [
                    {"name": "Typhoon Prototypes", "value": n_shots},
                    {"name": "Ice Storm Prototypes", "value": n_shots},
                    {"name": "Heatwave Prototypes", "value": n_shots},
                    {"name": "Accident Trajectory", "value": n_steps}
                ]
            }
        }
        return jsonify(frontend_payload), 200

    except Exception as e:
        logging.error(f"MATLAB 推演执行失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5026, debug=False)