// DOM Elements
      const loadingState = document.getElementById("loadingState");
      const contentState = document.getElementById("contentState");

      // Initialize Chart
      const ctx = document.getElementById("analyticsChart").getContext("2d");
      let analyticsChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: ["Approved", "Pending"],
          datasets: [
            {
              data: [0, 0],
              backgroundColor: ["#4caf50", "#ff9800"],
              borderWidth: 2,
              borderColor: "#ffffff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                padding: 20,
                usePointStyle: true,
                pointStyle: "circle",
                font: {
                  family: "Poppins",
                  size: 12,
                },
              },
            },
            title: {
              display: true,
              text: "Submission Status Overview",
              font: {
                family: "Poppins",
                size: 16,
                weight: "600",
              },
              padding: 20,
            },
          },
          cutout: "60%",
          animation: {
            animateScale: true,
            animateRotate: true,
          },
        },
      });

      async function fetchAnalytics() {
        try {
          const response = await fetch("/analytics_api/");
          const data = await response.json();

          if (data.error) {
            console.error(data.error);
            return;
          }

          // Hide loading state and show content after first load
          if (loadingState.style.display !== "none") {
            loadingState.style.display = "none";
            contentState.style.display = "block";
          }

          // Update text stats
          document.getElementById("totalCount").textContent = data.total_count;
          document.getElementById("pendingCount").textContent =
            data.pending_count;
          document.getElementById("approvedCount").textContent =
            data.approved_count;
          document.getElementById("approvalRate").textContent =
            data.approval_rate + "%";

          // Update chart with smooth transition
          analyticsChart.data.datasets[0].data = [
            data.approved_count,
            data.pending_count,
          ];
          analyticsChart.update("active");
        } catch (error) {
          console.error("Error fetching analytics:", error);

          // Show error state
          if (loadingState.style.display !== "none") {
            loadingState.innerHTML = `
            <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #dc3545;"></i>
            <p>Failed to load analytics data</p>
            <button onclick="location.reload()" style="
              background: var(--gradient);
              color: white;
              border: none;
              padding: 10px 20px;
              border-radius: 8px;
              font-family: 'Poppins';
              font-weight: 600;
              cursor: pointer;
              margin-top: 10px;
            ">
              <i class="fas fa-redo"></i>
              Try Again
            </button>
          `;
          }
        }
      }

      // Fetch data initially
      fetchAnalytics();

      // Refresh every 10 seconds
      setInterval(fetchAnalytics, 10000);