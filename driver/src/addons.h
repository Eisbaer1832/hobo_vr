// SPDX-License-Identifier: GPL-2.0-only

// Copyright (C) 2020-2021 Oleg Vorobiov <oleg.vorobiov@hobovrlabs.org>

#ifndef __HOBO_VR_ADDONS
#define __HOBO_VR_ADDONS

#include <openvr_driver.h>
#include "driverlog.h"
#include "hobovr_device_base.h"
#include "packets.h"
#include <utility>
#include <vector>

// #include <shoom.h>

// #include <thread>

//-----------------------------------------------------------------------------
// Purpose: eye tracking addon device, code name: Gaze Master
//-----------------------------------------------------------------------------

class GazeMasterDriver: public hobovr::HobovrDevice<false, false> {
public:
    GazeMasterDriver(std::string myserial);

    virtual vr::EVRInitError Activate(vr::TrackedDeviceIndex_t unObjectId) final;

    virtual void UpdateState(void* data) final;
    inline virtual size_t GetPacketSize() final {return sizeof(HoboVR_GazeState_t);}


private:

    void updateStatus(const uint16_t status); // status is EHoboVR_GazeStatus enum

    float smooth1D(float val);
    std::pair<float, float> smooth2D(float vec[2]);

    std::vector<float> m_smooth_buff_1D;
    std::vector<std::pair<float, float>> m_smooth_buff_2D;
    static constexpr int smooth_buff_size_max = 100;

    vr::VRInputComponentHandle_t m_pupil_pos_l[2];
    vr::VRInputComponentHandle_t m_pupil_pos_r[2];
    vr::VRInputComponentHandle_t m_eye_closed[2];
    vr::VRInputComponentHandle_t m_pupil_dilation[2];

};



//-----------------------------------------------------------------------------
// Purpose: (WIP) face tracking addon device, code name: Smile Driver
//-----------------------------------------------------------------------------

class SmileDriver: public hobovr::HobovrDevice<false, false> {
public:
    SmileDriver(std::string myserial);

    void UpdateState(void* data) override;
    size_t GetPacketSize() override;
};

#endif // #ifndef __HOBO_VR_ADDONS