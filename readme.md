### **Project Title:**  
**5G Standalone Network Simulation with Complete Protocol Stack, Interfaces, and Network Functions**

### **Objective:**
To design and implement a 5G standalone network that includes all key protocols, interfaces, and network functions, based on 3GPP standards. This network will simulate real-world 5G communication for testing, validation, and research purposes.

### **Project Components:**

#### 1. **Core Network Functions (CNFs)**
   - Implement the essential 5G core network functions with RESTful HTTP/2-based SBI for control plane signaling.
   - **Key Network Functions:**
     - **AMF (Access and Mobility Management Function):** Handles registration, authentication, and mobility.
     - **SMF (Session Management Function):** Manages sessions and traffic flows, using PFCP for user plane control with the UPF.
     - **UPF (User Plane Function):** Forwards data between the RAN and external data networks, using PFCP.
     - **PCF (Policy Control Function):** Enforces policies such as QoS and prioritization.
     - **UDM (Unified Data Management):** Manages subscriber data.
     - **AUSF (Authentication Server Function):** Authenticates devices and UEs.
     - **NEF (Network Exposure Function):** Exposes network services to third-party applications.
     - **UDR (Unified Data Repository):** Stores subscription and policy data.

#### 2. **RAN Components (gNB - Central Unit and Distributed Unit)**
   - **CU and DU Functions**:
     - Implement CU (Central Unit) and DU (Distributed Unit) of the 5G NR (New Radio) gNodeB.
     - **CU-CP** (Control Plane) and **CU-UP** (User Plane) components handle different layers (PDCP, RLC, MAC, PHY) based on the split RAN architecture.
   - **Key Interfaces**:
     - **N2**: Between RAN and AMF using NGAP over SCTP for control signaling.
     - **N3**: Between RAN and UPF using GTP-U for user data traffic.

#### 3. **User Equipment (UE)**
   - **5G Protocol Stack**: Includes NAS, PDCP, RLC, MAC, and PHY layers for signaling and user data.
   - **Signaling Protocol**:
     - **N1**: NAS signaling protocol over IP to communicate with the AMF.

#### 4. **Data Network (DN)**
   - Simulate an external data network for internet or enterprise services.
   - **N6 Interface**: Connects UPF to the Data Network using IP or Ethernet protocols.

#### 5. **Interface Layer Implementation**
   - Design each key interface with appropriate protocols:
     - **Control Plane**: N1, N2, N4, N5, N7, N8, N10, N11, N12, N13, N14, N15, and N16 interfaces with HTTP/2 and RESTful APIs.
     - **User Plane**: N3 (GTP-U), N6 (IP), and N9 (for UPF interconnections, if required).

#### 6. **Session and Policy Management**
   - **Session Management**: Implement PFCP for N4 interface to manage sessions in the UPF.
   - **Policy Control**: Use the PCF to enforce QoS and charging policies, communicating with SMF and AF using HTTP/2.

#### 7. **Testing and Validation**
   - **Traffic Simulation**: Use tools like Iperf and Ping to simulate different types of traffic (e.g., VoIP, video, and IoT data).
   - **Metrics Collection**: Monitor and log KPIs such as latency, throughput, packet loss, and jitter.
   - **Inter-Function Testing**: Validate protocol handling for each interface, including session establishment, QoS enforcement, and data forwarding.

### **Implementation Tools and Technologies:**
   - **Simulator/Emulator**: NS-3 with 5G-LENA module, extended for standalone 5G core functionalities.
   - **Programming Languages**: C++ for network functions, with Python for testing scripts and data analysis.
   - **Libraries**: Use Protobuf for message serialization, HTTP/2 libraries for RESTful API communications, and GTP-U and SCTP libraries for user and control planes, respectively.

### **Project Phases:**
   1. **Phase 1**: Setup of basic network functions (AMF, SMF, UPF) and simple connectivity between UE and DN.
   2. **Phase 2**: Implement core interfaces and protocols for end-to-end data flow.
   3. **Phase 3**: Add policy control, session management, and QoS handling with the PCF and other network functions.
   4. **Phase 4**: Finalize RAN (gNB-CU and DU), simulate real-world traffic, and perform testing for performance metrics.

### **Expected Outcome:**
A fully functional 5G standalone network simulation that accurately models 5G’s protocol stack, interfaces, and network functions, enabling advanced testing, research, and analysis of 5G systems and applications.

