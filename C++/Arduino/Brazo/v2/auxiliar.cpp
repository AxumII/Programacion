#include "Kinematic.h"

Kinematic::Kinematic(float _l1, float _l2, float _l3, 
                     float _w1, float _w2, float _w3, 
                     int _toolType, float _lTool, float _wTool, float _thetaTool) 
    : l1(_l1), l2(_l2), l3(_l3),
      w1(_w1), w2(_w2), w3(_w3), toolType(_toolType) 
{
    lTool = _lTool;
    wTool = _wTool;
    theta4 = _thetaTool* 180.0 / PI;

}

bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &phi ) {
    float W = w2 + w3 + wTool;
    float r_xy_sq = (x * x) + (y * y);
    if (r_xy_sq < (W * W)) return false; 
    float raiz_w = std::sqrt(r_xy_sq - (W * W));
    float t1 = std::atan2(y, x) + std::atan2(W, raiz_w);

    float zRel = z - l1;
    float R = (x * std::cos(t1)) + (y * std::sin(t1)) - w1;

    float R_wrist = R - lTool*cos(phi)
    float z_wrist = zRel - lTool*sin(phi)

    float D = ((R_wrist * R_wrist) + (z_wrist * z_wrist) - (l2 * l2) - (l3 * l3)) / (2.0 * l2 * l3);
    float t3_v = std::atan2(-std::sqrt(1.0 - (D * D)), D);
    float t3 = t3_v - beta;
    if (std::abs(D) > 1.0) return false;

    float beta = std::atan2(lTool * std::sin(theta4), l3 + lTool * std::cos(theta4));
        


    float t3 = t3_v - beta;
    float t2 = std::atan2(zRel, R) - std::atan2(L_virt * std::sin(t3_v), l2 + L_virt * std::cos(t3_v));

    th1 = t1 * 180.0 / PI;
    th2 = t2 * 180.0 / PI;
    th3 = t3 * 180.0 / PI;

    return true;
}