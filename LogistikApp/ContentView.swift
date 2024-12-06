import SwiftUI
import VisionKit
import Foundation

struct ContentView: View { //Type 'ContentView' does not conform to protocol 'View'
  
    
    
    @EnvironmentObject var vm: AppViewModel //Expected '}' in struct
    @Environment(\.presentationMode) var presentationMode
    
    @State private var alertTitle: String = "Info"
    @State private var teileNummer: String = ""
    @State private var filteredOrders: [Order] = []
    @State private var showDetailView: Bool = false
    @State private var showAlert = false
    @State private var showAlert1 = false
    @State private var alertMessage = ""
    @State private var alertMessage1 = ""
    @State private var scanCounter: Int = 0
    @State private var scannerViewID = UUID()
    @State private var showNoOrderAlert = false
    @State private var noOrderAlertMessage = ""
    private let textContentTypes: [(title: String, textContentType: DataScannerViewController.TextContentType?)] = [
        ("Teilenummer", .none),
    ]
    
    var body: some View {
        
        switch vm.dataScannerAccessStatus {
        case .scannerAvailable:
            mainView
        case .cameraNotAvailable:
            Text("Your device doesn't have a camera")
        case .scannerNotAvailable:
            Text("Your device doesn't have support for scanning with this app")
        case .cameraAccessNotGranted:
            Text("Please provide access to the camera in settings")
        case .notDetermined:
            Text("Requesting camera access")
        }
        
    }
    
    private var mainView: some View {
        NavigationView {
            DataScannerView(
                recognizedItems: $vm.recognizedItems,
                teileNummer: $vm.teileNummer,
                scanCounter: $vm.scanCounter,
                recognizedDataType: vm.recognizedDataType
            )
            .id(scannerViewID)
            .onAppear {
                scannerViewID = UUID()
            }
            .navigationBarTitle("Scanner", displayMode: .inline)
            // Inside ContentView.swift
            .onChange(of: vm.scanCounter) { _ in
                if let newTeileNummer = vm.teileNummer {
                    let formattedTeileNummer = switchNr(Teilenummer: newTeileNummer)
                    fetchOrdersByTeilenummer(teilenummer: formattedTeileNummer) { orders, errorMessage in
                        DispatchQueue.main.async {
                            if let orders = orders, !orders.isEmpty {
                                let result = filterOrdersByTeilenummer(Teilenummer: formattedTeileNummer, orders: orders)
                                // Sort the filtered orders by vehicle identification before setting them
                                self.filteredOrders = result.filteredOrders.sorted { $0.fahrzeugkennung ?? "" < $1.fahrzeugkennung ?? "" }
                                self.showAlert1 = result.deliveredAlert
                                if result.deliveredAlert {
                                    self.alertMessage1 = "Das Material mit der Teilenummer \(formattedTeileNummer) wurde bereits geliefert."
                                } else {
                                    self.showDetailView = true
                                }
                            } else {
                                self.showNoOrderAlert = true
                                self.noOrderAlertMessage = errorMessage ?? "Keine Bestellungen mit der Teilenummer \(formattedTeileNummer) gefunden."
                            }
                            teileNummer = ""
                        }
                    }
                }
            }
        }
               

                .background(
                    NavigationLink(destination: bottomContainerView.navigationBarBackButtonHidden(false), isActive: $showDetailView) {
                        EmptyView()
                    }.ignoresSafeArea()
                )
                .alert(isPresented: $showAlert1) {
                    Alert(
                        title: Text("Hinweis"),
                        message: Text(alertMessage1),
                        dismissButton: .default(Text("OK"))
                    )
                }
                .alert(isPresented: $showNoOrderAlert) {
                    Alert(
                        title: Text("Keine Bestellung gefunden"),
                        message: Text(noOrderAlertMessage),
                        dismissButton: .default(Text("OK"))
                    )
                }
            }
        }
    

    
        
        private var headerView: some View {
            VStack {
                if vm.scanType == .text {
                    Picker("Text content type", selection: $vm.textContentType) {
                        ForEach(textContentTypes, id: \.self.textContentType) { option in
                            Text(option.title).tag(option.textContentType)
                        }
                    }.pickerStyle(.segmented)
                }
                
                Text(vm.headerText).padding(.top)
            }.padding(.horizontal)
            
        }
        
        
        
    private var bottomContainerView: some View {
        List{
            ForEach(groupedAndSortedOrders.keys.sorted(), id: \.self) { fahrzeugkennung in
                Section(header: Text(fahrzeugkennung)) {
                    ForEach(groupedAndSortedOrders[fahrzeugkennung]!, id: \.id) { order in
                        VStack {
                            Text("Teilenummer: \(order.teilenummer!)")
                            Text("Menge: \(order.menge!)")
                            Text("Projekt: \(order.projekt!)").fontWeight(.bold)
                            
                                .fontWeight(.bold)
                            Button("Bestellung aktualisieren") {
                                
                                updateOrder(id: order.id!){
                                    success in
                                    showAlert = true
                                    alertMessage = success ? "Bestellung erfolgreich aktualisiert." : "Fehler bei der Aktualisierung der Bestellung."
                                }
                                
                                
                            }
                            
                            .foregroundColor()
                        }
                    header: {
                        Text(order.fahrzeugkennung!)
                        Text(order.projekt!)
                        
                    }
                    }
                }
                
                
                .padding(10)
                .listStyle(.insetGrouped)
                .alert(isPresented: $showAlert) {
                    Alert(
                        title: Text("Hinweis"),
                        message: Text(alertMessage),
                        dismissButton: .default(Text("OK"))
                    )
                }
            }
        }
        
        
