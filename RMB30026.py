from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 核心算法：直接用 numpy 替代原来的 MATLAB RMB261.m ---
def generate_knowledge_graph_data():
    n_shots = 5
    n_steps = 20

    # 1. 生成空间数据 (对应 MATLAB 的 rng(42) 和 randn)
    np.random.seed(42)
    proto_centers = np.array([[2, 5], [6, 2], [7, 7]])
    
    support_typ = proto_centers[0, :] + 0.6 * np.random.randn(n_shots, 2)
    support_ice = proto_centers[1, :] + 0.6 * np.random.randn(n_shots, 2)
    support_hea = proto_centers[2, :] + 0.6 * np.random.randn(n_shots, 2)

    proto_typ = np.mean(support_typ, axis=0)
    proto_ice = np.mean(support_ice, axis=0)
    proto_hea = np.mean(support_hea, axis=0)

    # 2. 模拟动态轨迹 (对应 MATLAB 的 linspace 和 sin/cos)
    t = np.linspace(0, 1, n_steps)
    traj_x = 1.5 + 4 * t + 0.3 * np.sin(10 * t)
    traj_y = 1.5 + 0.8 * t**2 + 0.2 * np.cos(10 * t)
    
    return (support_typ, support_ice, support_hea, 
            proto_typ, proto_ice, proto_hea, 
            traj_x, traj_y, n_shots, n_steps)

@app.route('/run_matlab', methods=['GET', 'POST'])
def get_knowledge_graph_data():
    try:
        # 直接调用 Python 算法，无需等待 MATLAB 引擎！
        res = generate_knowledge_graph_data()

        # 解析并转换为 JSON 需要的 list 格式
        support_typ = res[0].tolist()
        support_ice = res[1].tolist()
        support_hea = res[2].tolist()

        proto_typ = res[3].tolist()
        proto_ice = res[4].tolist()
        proto_hea = res[5].tolist()

        dynamic_trajectory = [[float(x), float(y)] for x, y in zip(res[6], res[7])]

        n_shots = int(res[8])
        n_steps = int(res[9])

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
        logging.error(f"执行失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5026, debug=False)
