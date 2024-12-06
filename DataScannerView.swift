//  DataScannerView.swift
//  LogistikApp
//
//  Created by Fatime Al-Batat on 10/12/23.
//
import Foundation
import SwiftUI
import VisionKit

struct DataScannerView: UIViewControllerRepresentable {
    
    @EnvironmentObject var vm: AppViewModel
    @State private var isScannerActive = false
    @Binding var recognizedItems: [RecognizedItem]
    @Binding var teileNummer: String?
    @Binding var scanCounter: Int
    
    let recognizedDataType: DataScannerViewController.RecognizedDataType
    
    func makeUIViewController(context: Context) -> DataScannerViewController {
        let vc = DataScannerViewController(
            recognizedDataTypes: [recognizedDataType],
            qualityLevel: .balanced,
            recognizesMultipleItems: true,
            isPinchToZoomEnabled: true,
            isGuidanceEnabled: true,
            isHighlightingEnabled: true
        )
        return vc
    }
    
    func updateUIViewController(_ uiViewController: DataScannerViewController, context: Context) {
        uiViewController.delegate = context.coordinator
             
                      try? uiViewController.startScanning()
                      
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(
            recognizedItems:  $recognizedItems,
            teileNummer: $teileNummer,
            scanCounter: $scanCounter
           
        )
    }
    
   
    
    //Koordinator
    class Coordinator: NSObject, DataScannerViewControllerDelegate {
        @Binding var recognizedItems: [RecognizedItem]
        @Binding var teileNummer: String?
        @EnvironmentObject var vm: AppViewModel
        @Binding var scanCounter: Int
        
        init(recognizedItems: Binding<[RecognizedItem]>, teileNummer: Binding<String?>, scanCounter: Binding<Int>) {
            self._recognizedItems = recognizedItems
            self._teileNummer = teileNummer
            self._scanCounter = scanCounter
            
        }
        
        // Delegate: didTapOn
        func dataScanner(_ dataScanner: DataScannerViewController, didTapOn item: RecognizedItem) {
            print("didTapOn \(item)")
            if case .text(let text) = item {
                // Copy the text to the pasteboard.
                UIPasteboard.general.string = text.transcript
            }
        }
        
        func dataScanner(_ dataScanner: DataScannerViewController, didAdd addedItems: [RecognizedItem], allItems: [RecognizedItem]) {
            
            UINotificationFeedbackGenerator().notificationOccurred(.success)
            for addedItem in addedItems {
                
                if case .text(let text) = addedItem {
                    // Teile den gescannten Text in Zeilen auf
                    let lines = text.transcript.components(separatedBy: .newlines)
                    let pattern = "(H\\.KH\\.[0-9]{3}\\.[0-9]{3}\\.[0-9]{2}\\.[0-9]{2}(?:\\.[0-9]{2})?)|([A,N]{1}[\\.\\s][0-9]{3}[\\.\\s][0-9]{3}[\\.\\s][0-9]{2}[\\.\\s][0-9]{2}(?:[\\.\\s][0-9]{2})?)|([N]{1}[\\.\\s][0-9]{6}[\\.\\s][0-9]{6})|(U\\.[0-9]{6}\\.[0-9A-Za-z]{6})"
                    
                    for line in lines {
                        if let range = line.range(of: pattern, options: .regularExpression) {
                            teileNummer = String(line[range])
                            scanCounter += 1
                            print("Gefundene Teilenummer: \(teileNummer)")
                            break
                        }
                    }
                    
                }
            }
        }
        
        // Delegate: didRemove
        func dataScanner(_ dataScanner: DataScannerViewController, didRemove removedItems: [RecognizedItem], allItems: [RecognizedItem]) {
            self.recognizedItems = recognizedItems.filter { item in
                !removedItems.contains(where: {$0.id == item.id })
            }
        }
        
        // Delegate: unavailable
        func dataScanner(_ dataScanner: DataScannerViewController, becameUnavailableWithError error: DataScannerViewController.ScanningUnavailable) {
            print("became unavailable with error \(error.localizedDescription)")
        }
    }
}
