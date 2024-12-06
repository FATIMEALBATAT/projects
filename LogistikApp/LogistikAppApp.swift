//
//
// 
//
//  Created by Fatime Al-Batat on 10/12/23.

//

import SwiftUI

@main
	struct LogistikAppApp: App {
    
    @StateObject private var vm = AppViewModel()
    @State private var showHomeView = true
    
    var body: some Scene {
        WindowGroup {

            if showHomeView {
                           HomeView()
                               .environmentObject(vm)
                               .onTapGesture {
                                   
                                       showHomeView = false
                                   
                               }
                       } else {
                           ContentView()
                               .environmentObject(vm)
                               .task {
                                   await vm.requestDataScannerAccessStatus()
                               }
                       }
            
                   }
        }
    }

