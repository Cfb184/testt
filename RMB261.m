function [support_typ, support_ice, support_hea, proto_typ, proto_ice, proto_hea, traj_x, traj_y, n_shots, n_steps] = RMB261()
% 极端天气小样本学习引导的事故动态知识库 (纯数据生成，无GUI)

% 数据量定义
n_shots = 5;      
n_steps = 20;     

% --- 生成空间数据 ---
rng(42); 
proto_centers = [2, 5; 6, 2; 7, 7]; 
support_typ = proto_centers(1,:) + 0.6 * randn(n_shots, 2);
support_ice = proto_centers(2,:) + 0.6 * randn(n_shots, 2);
support_hea = proto_centers(3,:) + 0.6 * randn(n_shots, 2);

proto_typ = mean(support_typ);
proto_ice = mean(support_ice);
proto_hea = mean(support_hea);

% --- 模拟动态轨迹 ---
t = linspace(0, 1, n_steps);
traj_x = 1.5 + 4 * t + 0.3 * sin(10*t);
traj_y = 1.5 + 0.8 * t.^2 + 0.2 * cos(10*t);

% 注意：绝对不能包含任何 figure, plot, pie, scatter 命令
end