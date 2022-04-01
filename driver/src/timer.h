// SPDX-License-Identifier: GPL-2.0-only

// Copyright (C) 2020-2021 Oleg Vorobiov <oleg.vorobiov@hobovrlabs.org>

#ifndef __HOBO_VR_TIMER
#define __HOBO_VR_TIMER

#include <atomic>
#include <thread>
#include <mutex>
#include <memory>
#include <vector>
#include <functional>
#include <chrono>
#include <ctime>

namespace hobovr {

using namespace std::chrono_literals;

class Timer {
public:
	Timer();
	~Timer();

	// no moving/coping this object
	Timer(const Timer&) = delete;
	Timer(Timer&&) = delete;
	Timer& operator= (Timer) = delete;
	Timer& operator= (Timer&&) = delete;

	template<class Rep, class Duration>
	void registerTimer(const std::chrono::duration<Rep, Duration>& delay, std::function<void(void)> func);

	template<class Rep, class Duration>
	void setGlobalDelay(const std::chrono::duration<Rep, Duration>& delay);

	std::chrono::nanoseconds getGlobalDelay();

private:
	void internal_thread();

	std::unique_ptr<std::thread> m_thread;

	std::mutex m_mutex;
	std::atomic<bool> m_alive{true};

	std::atomic<std::chrono::nanoseconds> m_delay{10s};
	std::vector<std::pair<std::function<std::chrono::nanoseconds(void)>, std::chrono::nanoseconds>> m_timers;
};

} // namespace hobovr

#endif // #ifndef __HOBO_VR_TIMER